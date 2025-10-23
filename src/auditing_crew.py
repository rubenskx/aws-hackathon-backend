from bedrock_agentcore.runtime import BedrockAgentCoreApp
from src.crew import LatestAiDevelopmentCrew
from prompts.predictor import create_prompt
import os


# ---------- Agentcore imports --------------------

app = BedrockAgentCoreApp()
# ------------------------------------------------

markdown_file_path = "uploads/hcl.md"
transaction_file_path = "data/transactions.md"

@app.entrypoint
def agent_invocation(payload, context):
    """Handler for agent invocation"""
    print(f'Payload: {payload}')
    try:
        # Extract user message from payload with default
        user_message = payload.get(
            "markdown", "Artificial Intelligence in Healthcare")
        print(f"Processing topic: {user_message}")

        # Create crew instance and run synchronously
        auditing_crew = LatestAiDevelopmentCrew()
        crew = auditing_crew.crew()
        try:
            # Open the Markdown file in read mode with UTF-8 encoding
            with open(markdown_file_path, 'r', encoding='utf-8') as f:
                markdown_text = f.read()
            with open(transaction_file_path, 'r', encoding="utf-8") as f:
                transaction_data = f.read()

        except Exception as e:
            print(f"An error occurred: {e}")
            markdown_text = ""
            transaction_data = ""

        inputs = {
            'financial_statement': markdown_text,
            'transaction_data': transaction_data,
            'prediction_prompt': create_prompt(markdown_text)
        }
        
        result = crew.kickoff(inputs=inputs)

        print("Context:\n-------\n", context)
        print("Result Raw:\n*******\n", result.raw)

        # Safely access json_dict if it exists
        if hasattr(result, 'json_dict'):
            print("Result JSON:\n*******\n", result.json_dict)

        return {"result": result.raw}

    except Exception as e:
        print(f'Exception occurred: {e}')
        return {"error": f"An error occurred: {str(e)}"}


if __name__ == "__main__":
    app.run()
