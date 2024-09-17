# Functions Folder For The Engine
import os
from openai import AzureOpenAI
import numpy as np
import openai
import sqlite3
from dotenv import load_dotenv
from pdfminer.high_level import extract_text as pdf_extract_text
import glob


def initialize_openai():
    """Initialize OpenAI API key."""
    load_dotenv()
    client = AzureOpenAI(
        azure_endpoint="https://jubgpt.openai.azure.com/",
        api_key="a0f2977d9a3b4ff1899948650",
        api_version="2024-02-01",
    )


def initialize_sqlite_connection():
    """Initialize SQLite connection."""
    db_path = os.getenv("SQLITE_DB_PATH", "sqlite:///pdf_db.sqlite")
    conn = sqlite3.connect(db_path)
    return conn


def detect_malicious_intent(question: str) -> tuple:
    """Uses OpenAI's moderation model to detect malicious intent in a question."""
    try:
        response = openai.Moderations.create(
            model="text-moderation-latest", input=question
        )
        is_flagged = response["results"][0]["flagged"]
        return is_flagged, (
            "This question has been flagged for malicious content and cannot be processed."
            if is_flagged
            else "No malicious intent detected."
        )
    except Exception as e:
        return None, f"Error in moderation: {str(e).split('. ')[0]}."


def query_database(query: str) -> tuple:
    """Executes a given query on the database."""
    conn = initialize_sqlite_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        return result if result else None
    finally:
        conn.close()


def question_to_embeddings(question: str) -> list:
    """Converts a question to embeddings."""
    try:
        response = openai.Embeddings.create(
            input=question, model="text-embedding-3-large"
        )
        embedded_query = response["data"][0]["embedding"]
        if len(embedded_query) != 3072:
            raise ValueError(
                "The dimensionality of the question embedding does not match the expected 3072 dimensions."
            )
        return np.array(embedded_query, dtype=np.float64).tolist()
    except Exception as e:
        print(f"Error embedding the question: {e}")
        return []


def check_relatedness_to_pdf_content(question: str) -> tuple:
    """Checks if the question is related to the PDF content by querying a database."""
    question_vectorized = question_to_embeddings(question)
    conn = initialize_sqlite_connection()
    try:
        cursor = conn.cursor()
        sql_query = """
            SELECT id, text, embedding <=> CAST(? AS BLOB) AS distance 
            FROM pdf_holder
            ORDER BY distance ASC
            LIMIT 1;
        """
        cursor.execute(
            sql_query, (np.array(question_vectorized, dtype=np.float64).tobytes(),)
        )
        result = cursor.fetchone()
        if result:
            closest_id, _, distance = result
            threshold = 0.5
            if distance < threshold:
                return True, "Question is related to the PDF content."
            else:
                return False, "Question is not related to the PDF content."
        else:
            return False, "No match found in the database."
    except Exception as e:
        print(f"Error searching the database: {e}")
        return False, f"Error searching the database: {e}"
    finally:
        conn.close()


def process_user_question() -> tuple:
    """Main function to start the question processing workflow."""
    initialize_openai()
    while True:
        question = input("Enter your question or type 'exit' to quit: ").strip()
        if question.lower() == "exit":
            print("Exiting...")
            return None

        is_flagged, message = detect_malicious_intent(question)
        print(message)
        if is_flagged or is_flagged is None:
            continue
        related, message = check_relatedness_to_pdf_content(question)
        print(message)
        if related:
            return question_to_embeddings(question), question
        else:
            print("Please try a different question...")


def generate_response(question: str, retrieved_info: str) -> str:
    """Generates a response from OpenAI's ChatCompletion based on facts and a user question."""
    response = openai.Completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"Based on the FACTS, give a concise and detailed answer to the QUESTION.\nQUESTION: {question}\nFACTS: {retrieved_info}",
            }
        ],
    )
    if response["choices"]:
        return response["choices"][0]["message"]["content"]
    print("No content available.")
    return ""


def pdf_to_text(pdf_path: str, chunk_length: int = 1000) -> list:
    """Extracts text from a PDF and generates embeddings."""
    text = pdf_extract_text(pdf_path)
    chunks = [
        text[i : i + chunk_length].replace("\n", "")
        for i in range(0, len(text), chunk_length)
    ]
    return generate_embeddings(chunks)


def generate_embeddings(chunks: list) -> list:
    """Generates embeddings for text chunks."""
    try:
        response = openai.Embeddings.create(model="gpt-4o-mini", input=chunks)
        return [
            {
                "vector": embedding_info["embedding"],
                "text": chunks[embedding_info["index"]],
            }
            for embedding_info in response["data"]
        ]
    except Exception as e:
        print(f"An error occurred during embeddings generation: {e}")
        return []


def define_vector_store(embeddings: list) -> bool:
    """Stores embeddings into the database."""
    conn = initialize_sqlite_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pdf_holder")  # Clear the table
        for embedding in embeddings:
            cursor.execute(
                "INSERT INTO pdf_holder (text, embedding) VALUES (?, ?)",
                (
                    embedding["text"],
                    sqlite3.Binary(
                        np.array(embedding["vector"], dtype=np.float64).tobytes()
                    ),
                ),
            )
        conn.commit()
        print("Embeddings successfully stored in the database.")
        return True
    except Exception as e:
        conn.rollback()
        print(f"An error occurred while storing embeddings: {e}")
        return False
    finally:
        conn.close()
