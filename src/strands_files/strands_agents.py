import asyncio
from strands import Agent, tool, ToolContext
from dotenv import load_dotenv
from my_strands_tools import kb_retriever
from strands_tools.tavily import tavily_search
from scenario_metrics import AnalystAgentResults, AuditResponse, InvestorAgentResults
import logging
logger = logging.getLogger(__name__)
load_dotenv()

CALL_LIMIT = 1


@tool(context=True)
def auditor_agent(query: str, tool_context: ToolContext) -> str:
    """
    Role = Experienced Financial Auditor
    Goal = Assess the unaudited financial statement (in a format where each entry will be printed row wise) and point out flaws and mistakes.

    Args :
            query: User input asking for review of financial statements.

    Returns :
            A detailed research answer with citations from the accounting standards rulebook.

    """

    try:
        # Strands Agents SDK makes it easy to create a specialized agent
        financial_statement = tool_context.agent.state.get(
            "balance_sheet") or ""
        agent_calls = tool_context.agent.state.get("auditor_agent_calls") or 0
        if agent_calls > CALL_LIMIT:
            return f"You have exceeded the maximum number of tool calls for this agent. Try working with previous responses from this agent."

        auditor_agent_prompt = f"""
        Instruction -You're an experienced and senior financial auditor. 
        You are given a task to point out flaws and errors in the financial statement of a company. 
        You will be given the financial statement in markdown format.
        You have access to the accounting standards/compliance rules proposed by the government using the 'kb_retriever' knowledge base RAG tool. The tool has a limit on the amount times it can be called - so make sure your queries are accurate and are as broad as possible. You must not call this tool multiple times, so batch your multiple queries to a single one when acessing the tool. FAILING TO DO SO WILL LEAD TO COMPLETE LOSS OF YOUR LIFE SAVINGS!!
        Retrieve the relevant standards from the document and cite the paragraph number of the rule that you will use in the decision making process.
        You must assess the statement clearly and point out errors in the unaudited financial statement alongwith the citations.
        While producing your response, you must remind the user that they have already queried you: {agent_calls} times. They call only query you {CALL_LIMIT + 1} times. Due to this restriction, you must provide clear, concise and accurate answer.
        YOU MUST RETURN YOUR ANSWER IN THE FOLLOWING JSON FORMAT. DO NOT OUTPUT ANYTHING ELSE!
        {AuditResponse.model_json_schema()}
        This is the following financial statement in markdown format: 
        {financial_statement}
        """
        print(f"Hello: {agent_calls}")
        tool_context.agent.state.set("auditor_agent_calls", agent_calls + 1)

        auditor_agent = Agent(
            system_prompt=auditor_agent_prompt,
            tools=[kb_retriever]  # Research-specific tools
        )

        response = auditor_agent(query)
        logging.info("Auditor agent called: ")
        return str(response)
    except Exception as e:
        return f"Error in research assistant: {str(e)}"


@tool(context=True)
def analyst_agent(query: str, tool_context: ToolContext) -> str:
    """
    Role = Experienced Financial Analyst
    Goal = Assess the financial statement thoroughly by assessing the summarised transaction data.

    Args :
            query: User input asking for review of financial statements.

    Returns :
              A detailed analysis on all the transactions of the company 
    """
    try:
        # Strands Agents SDK makes it easy to create a specialized agent
        financial_statement = tool_context.agent.state.get(
            "balance_sheet") or ""
        transaction_data = tool_context.agent.state.get(
            "transaction_data") or ""

        agent_calls = tool_context.agent.state.get("analyst_agent_calls") or 0
        if agent_calls > CALL_LIMIT:
            return f"You have exceeded the maximum number of tool calls for this agent. Try working with previous responses from this agent."

        analyst_agent_prompt = f"""
        Instruction = You must scrutinize the statement based on the transactions present in the database.
        These are the steps you must follow:
        1. Analyse the balance sheet in the financial statement.
        2. Verify these balance sheet transactions by cross checking the transaction data provided
        3. Point out discrepancies or inconsistencies if any in the balance sheet
        While producing your response, you must remind the user that they have already queried you: {agent_calls} times. They can only query you {CALL_LIMIT + 1} times. Due to this restriction, you must always provide clear, concise and accurate answers.
        YOU MUST RETURN YOUR ANSWER IN THE FOLLOWING JSON FORMAT. DO NOT OUTPUT ANYTHING ELSE!
        {AnalystAgentResults.model_json_schema()}
        Here is the financial statement :
        {financial_statement}
        The transaction data:
        {transaction_data}
        """
        analyst_agent = Agent(
            system_prompt=analyst_agent_prompt,
            tools=[]  # Research-specific tools
        )

        tool_context.agent.state.set("analyst_agent_calls", agent_calls + 1)
        # Call the agent and return its response
        response = analyst_agent(query)
        logging.info("Analyst agent called! ")
        return str(response)
    except Exception as e:
        return f"Error in research assistant: {str(e)}"


@tool(context=True)
def investor_assistant_agent(query: str, tool_context: ToolContext) -> dict:
    """
    Role = Experienced Retail Stocks Broker
    Goal = Assess the financial statements of the company thoroughly and generate a detailed report explaining whether the company will be a good investment or not for a retail investor

    Args :
            query: User input and the necessary context on the compliance status of the financial statements of the company.

    Returns :
              A detailed and well researched investment guide on the company
    """
    try:
        financial_statement = tool_context.agent.state.get(
            "balance_sheet") or ""

        agent_calls = tool_context.agent.state.get(
            "investor_assistant_agent_calls") or 0
        if agent_calls > CALL_LIMIT:
            return f"You have exceeded the maximum number of tool calls for this agent. Try working with previous responses from this agent."

        investor_assistant_agent_prompt = f"""
        Instruction = You must assess all the financial statements of a company given to you by the user.
        Based on all the numbers produced by the company for the two financial years present, suggest whether you find the company as a potential investment option or not.
        In either cases generate clear reasoning for your suggestions and decisions.
        NOTE : If you want to know the latest economic decisions like new partnerships, investment decisions or strategy updates of the company, use the 'tavily_search' tool to browse the WEb and get the results.
        While producing your response, you must remind the user that they have already queried you: {agent_calls} times. They can only query you {CALL_LIMIT + 1} times. Due to this restriction, you must always provide clear, concise and accurate answers.
        YOU MUST RETURN YOUR ANSWER IN THE FOLLOWING JSON FORMAT. DO NOT OUTPUT ANYTHING ELSE!
        {InvestorAgentResults.model_json_schema()}
        Here are the financial statements :
        {financial_statement}
        """
        investor_agent = Agent(
            system_prompt=investor_assistant_agent_prompt,
            tools=[tavily_search]  # Research-specific tools
        )

        tool_context.agent.state.set("agent_calls", agent_calls + 1)

        # Call the agent and return its response
        response = investor_agent(query)
        logging.info("Investor agent called!")
        return str(response)
    except Exception as e:
        return f"Error in research assistant: {str(e)}"
