import asyncio
from strands import Agent, tool, ToolContext
from dotenv import load_dotenv
from my_strands_tools import kb_retriever
from strands_tools.tavily import tavily_search
load_dotenv()

@tool(context=True)
async def auditor_agent(query:str,tool_context: ToolContext)->str:
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
        financial_statement= tool_context.agent.state.get("balance_sheet") or ""
        auditor_agent_prompt =f"""
        Instruction -You're an experienced and senior financial auditor. 
        You are given a task to point out flaws and errors in the financial statement of a company. 
        You will be given the financial statement in markdown format.
        You have access to the accounting standards/compliance rules proposed by the government using the 'kb_retriever' tool.
        Retrieve the relevant standards from the document and cite the paragraph number of the rule that you will use in the decision making process.
        You must assess the statement clearly and point out errors in the unaudited financial statement alongwith the citations.
        This is the following financial statement in markdown format: 
        {financial_statement}
        """
        auditor_agent = Agent(
            system_prompt=auditor_agent_prompt,
            tools=[kb_retriever]  # Research-specific tools
        )


        response = await auditor_agent(query)
        return str(response)
    except Exception as e:
        return f"Error in research assistant: {str(e)}"
    

@tool(context=True)
def analyst_agent(query:str,tool_context: ToolContext)->str:
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
        financial_statement = tool_context.agent.state.get("balance_sheet") or ""
        transaction_data = tool_context.agent.state.get("transaction_data") or ""

        analyst_agent_prompt =f"""
        Instruction = You must scrutinize the statement based on the transactions present in the database.
        These are the steps you must follow:
        1. Analyse the balance sheet in the financial statement.
        2. Verify these balance sheet transactions by cross checking the transaction data provided
        3. Point out discrepancies or inconsistencies if any in the balance sheet
        Here is the financial statement :
        {financial_statement}
        The transaction data:
        {transaction_data}
        """
        analyst_agent = Agent(
            system_prompt=analyst_agent_prompt,
            tools=[]  # Research-specific tools
        )

        # Call the agent and return its response
        response = analyst_agent(query)
        return str(response)
    except Exception as e:
        return f"Error in research assistant: {str(e)}"
    

@tool(context=True)
def investor_assistant_agent(query:str,tool_context: ToolContext)->str:
    """
    Role = Experienced Retail Stocks Broker
    Goal = Assess the financial statements of the company thoroughly and generate a detailed report explaining whether the company will be a good investment or not for a retail investor

    Args :
            query: User input and the necessary context on the compliance status of the financial statements of the company.

    Returns :
              A detailed and well researched investment guide on the company
    """
    try:
        financial_statement = tool_context.agent.state.get("balance_sheet") or ""
        
        investor_assistant_agent_prompt =f"""
        Instruction = You must assess all the financial statements of a company given to you by the user.
        Based on all the numbers produced by the company for the two financial years present, suggest whether you find the company as a potential investment option or not.
        In either cases generate clear reasoning for your suggestions and decisions.
        NOTE : If you want to know the latest economic decisions like new partnerships, investment decisions or strategy updates of the company, use the 'tavily_search' tool to browse the WEb and get the results.
        Here are the financial statements :
        {financial_statement}
        """
        analyst_agent = Agent(
            system_prompt=investor_assistant_agent_prompt,
            tools=[tavily_search]  # Research-specific tools
        )

        # Call the agent and return its response
        response = analyst_agent(query)
        return str(response)
    except Exception as e:
        return f"Error in research assistant: {str(e)}"
    

@tool(context=True)
def report_writer_agent(query:str)->str:
    """
    Role = Financial Report Writer
    Goal = Assess the decisions taken by the Auditor, Analyst and Investor agent to come up with the final report that should be send to the user.

    Args :
            query : The detailed decisions taken by each of the auditor, analyst and investment assistant agent should be made available to the report generation agent.

    Returns :
              A detailed output report for the user elaborating all the findings from the research

    """
    try:
        report_generation_prompt = """
        Instruction = You must first understand the decision taken by Auditor, Analyst and Investor agent. 
        Based on the feedback provided by these agents , you should do the following :
        1. A descriptive and informative report on the financial health identifying the strong points of the financials of the company and the major areas to watch out for in the next yearly performance of the company. :: if company's financial statements are error-free
        2. A descriptive and informative report informing the user that it is in best interest to wait to invest in the company as there are some errors in it's financials.Also include the identified errors in the financial statements alongwith the citations to the rules from accounting standards in the report. :: else if company's financial statements have errors
        Note - Do not use complex financial jargon. Use simple language and explain nuances in detail for the retail investor.
        """


        analyst_agent = Agent(
            system_prompt=report_generation_prompt,
            tools=[]  # Research-specific tools
        )

        # Call the agent and return its response
        response = analyst_agent(query)
        return str(response)
    except Exception as e:
        return f"Error in research assistant: {str(e)}"