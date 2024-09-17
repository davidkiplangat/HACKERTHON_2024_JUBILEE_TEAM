# Importing the Required PKGS
import os
import numpy as np
import openai
import sqlite3
from dotenv import load_dotenv
from pdfminer.high_level import extract_text as pdf_extract_text
import glob
from functions import *


def process_pre_run(pdf_folder_path: str) -> bool:
    """Processes PDF files and stores embeddings."""
    pdf_file_paths = glob.glob(os.path.join(pdf_folder_path, "*.pdf"))
    if not pdf_file_paths:
        print("No PDF files found in the specified directory.")
        return False

    for pdf_file_path in pdf_file_paths:
        embeddings = pdf_to_text(pdf_file_path)
        if not embeddings or not define_vector_store(embeddings):
            print(f"Failed to store embeddings for {pdf_file_path}.")
            return False

    return True


def main():
    """Main function to run the complete workflow."""
    DIRECTORY_PATH = r"C:\Users\DaviSki\Downloads\Compressed\code\Documents"

    if process_pre_run(DIRECTORY_PATH):
        vectorized_question, original_question = process_user_question()
        if vectorized_question:
            retrieved_info = process_retrieval(vectorized_question)
            final_response = generate_response(original_question, retrieved_info)
            print("\n")
            print("********** Question **********")
            print("\n")
            print(f"{original_question}")
            print("\n")
            print("********** Answer **********")
            print("\n")
            print(f"{final_response}")
        else:
            print("No question was processed successfully.")
    else:
        print("Pre-run service failed. Please check the setup and try again.")


if __name__ == "__main__":
    main()
