import time
from dotenv import load_dotenv
from strands import Agent
from strands.tools.executors import ConcurrentToolExecutor
from strands_agents import auditor_agent, analyst_agent, investor_assistant_agent
import logging
from strands.models import BedrockModel
from dotenv import load_dotenv
from scenario_metrics import ReportModel
from logging_config import setup_logging
import os
setup_logging()
logger = logging.getLogger(__name__)


load_dotenv()
CALL_LIMIT = 1
start_time = time.time()



MAIN_SYSTEM_PROMPT = f"""
You are a task supervisor that decomposes and delegates tasks to specialized agents:
- For validating financial statements against the government authorized auditing standards → Use the auditor_agent tool
- For validating financial statements against the company's transaction records  → Use the analyst_agent tool
- For generating investment advice for the user about the company he has asked → Use the investor_assistant_agent tool


Whenever the tool agent responds maximum tool call message, you must work with previous responses of the agent, and stop calling that agent again.
YOU MUST CALL THE AGENTS ONLY WHEN ABSOLUTELY REQUIRED AND PROVIDE ACCURATE QUERIES.THERE IS A MAXIMUM NO OF {CALL_LIMIT} CALLS AVAILABLE TO EACH AGENT. MAKE YOUR QUERIES ARE BROAD AND YOU MUST WORK WITH THE CONTEXT TO PROVIDE A QUICK, CONCISE AND ACCURATE RESPONSE.
Always select the most appropriate tool based on the user's query.
YOU MUST RETURN THE FINAL OUTPUT IN THE FOLLOWING JSON FORMAT
{ReportModel.model_json_schema()}
"""
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"  # Set before creating the model

bedrock_model = BedrockModel(
    model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    temperature=0.1,
    streaming=False
)


balance_sheet_path = r"F:\udemy\langchain\langgraph\aws-hackathon-backend\src\data\hcl.md"
transactions_path = r"F:\udemy\langchain\langgraph\aws-hackathon-backend\src\data\transactions.md"
cashflows_path = ""
income_path = ""


with open(balance_sheet_path, 'r', encoding='utf-8') as f:
    balance_sheet = f.read()
with open(transactions_path, 'r', encoding="utf-8") as f:
    transaction_data = f.read()

state = {'balance_sheet': balance_sheet, 'cashflows': "", 'income': "",
         'transaction_data': transaction_data, 'kb_calls': 0, 'auditor_agent_calls': 0, 'analyst_agent_calls': 0, 'investor_assistant_agent_calls': 0}

logger.info("Main program started!!")

orchestrator = Agent(
    tool_executor=ConcurrentToolExecutor(),
    model=bedrock_model,
    state=state,
    system_prompt=MAIN_SYSTEM_PROMPT,
    callback_handler=None,
    tools=[auditor_agent, analyst_agent,
           investor_assistant_agent]
)



input_mssg = """I have given you the balance sheet of HCL Technologies collected from their website.
Please analyse it for errors and understand the financial state of the company. The financial statement data is available and provided to all the agents."""

response = orchestrator(input_mssg)
structured_results = orchestrator.structured_output(
    ReportModel,
    response.message['content'][0]['text']
)
end_time = time.time()  # record end time

duration = end_time - start_time

if __name__ == '__main__':
    print(f"Crew Initiated with message {input_mssg}\n")
    # print(f"Results {response.message['content'][0]['text']}")
    print(structured_results)
    print(f"Task completed in {duration:.4f} seconds")
