#!/usr/bin/env python
# src/latest_ai_development/main.py
import sys
from crew import LatestAiDevelopmentCrew

markdown_file_path = "uploads/hcl.md"
transaction_file_path = "data/transactions.md"


def run():
    """
    Run the crew.
    """
    try:
        # Open the Markdown file in read mode with UTF-8 encoding
        with open(markdown_file_path, 'r', encoding='utf-8') as f:
            markdown_text = f.read()
        with open(transaction_file_path, 'r', encoding="utf-8") as f:
            transaction_data = f.read()

    except Exception as e:
        print(f"An error occurred: {e}")

    inputs = {
        'financial_statement': markdown_text,
        'transaction_data': transaction_data,
    }
    crew_output = LatestAiDevelopmentCrew().crew().kickoff(inputs=inputs)
    with open("output/report.txt", "w", encoding="utf-8") as f:
        f.write(crew_output.raw)
    print("Successfully saved!")


if __name__ == "__main__":
    run()
