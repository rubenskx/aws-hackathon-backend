from dotenv import load_dotenv
from strands import Agent
from strands_agents import auditor_agent,analyst_agent,investor_assistant_agent,report_writer_agent
import boto3
from strands.models import BedrockModel
from dotenv import load_dotenv
load_dotenv()


MAIN_SYSTEM_PROMPT = """
You are a task supervisor that decomposes and delegates tasks to specialized agents:
- For validating financial statements against the government authorized auditing standards → Use the auditor_agent tool
- For validating financial statements against the company's transaction records  → Use the analyst_agent tool
- For generating investment advice for the user about the company he has asked → Use the investor_assistant_agent tool
- For generating a report after the final analysis by all agents → Use the report_writer_agent

Always select the most appropriate tool based on the user's query.
"""

bedrock_model = BedrockModel(
    model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
    temperature=0.2,
)


balance_sheet_path = r"D:\AI projects\hackathon\aws-hackathon-backend\src\data\hcl.md"
transactions_path = r"D:\AI projects\hackathon\aws-hackathon-backend\src\data\transactions.md"
cashflows_path = ""
income_path = ""


with open(balance_sheet_path, 'r', encoding='utf-8') as f:
            balance_sheet = f.read()
with open(transactions_path, 'r', encoding="utf-8") as f:
            transaction_data = f.read()

state = {'balance_sheet': balance_sheet, 'cashflows':"", 'income':"", 'transaction_data': transaction_data}

orchestrator = Agent(
    model = bedrock_model,
    state = state,
    system_prompt=MAIN_SYSTEM_PROMPT,
    callback_handler=None,
    tools=[auditor_agent,analyst_agent,investor_assistant_agent,report_writer_agent]
)

input_mssg = """I have given you the balanche sheet of HCL Technologies collected from their website.
Please analyse it for errors and understand the financial state of the company"""

response = orchestrator(input_mssg)


if __name__=='__main__':
    print(f"Crew Initiated with message {input_mssg}\n")
    print(f"Results {response}")