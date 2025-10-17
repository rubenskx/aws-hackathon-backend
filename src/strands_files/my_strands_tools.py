import asyncio
import boto3
import json
from dotenv import load_dotenv
from strands import Agent, tool

load_dotenv()


@tool
async def kb_retriever(query:str) -> str:
    """
    Goal = Retrieves compliance guidelines from the knowledge base created with Accounting Standards relevant to the financial statements

    Args :
            query: A string specific about a particular entry from the financial statements, so that the we get the most accurate and relevant results from the knowledge base.

    Returns :
            A dictionary of the response and the rules/citations from the knowledge base
    """
    bedrock_agent_runtime = boto3.client(
                            service_name='bedrock-agent-runtime',
                            region_name='us-east-1'  # e.g., 'us-east-1', 'us-west-2'
                            )
    
    knowledge_base_id = 'O3IBGYPABF'
    model_id = 'arn:aws:bedrock:us-east-1:992382746523:inference-profile/us.anthropic.claude-3-7-sonnet-20250219-v1:0'

    response = bedrock_agent_runtime.retrieve_and_generate(
        input={
            'text': query
        },
        retrieveAndGenerateConfiguration={
            'type': "KNOWLEDGE_BASE",
            'knowledgeBaseConfiguration': {
                'knowledgeBaseId': knowledge_base_id,
                'modelArn': model_id,
            }
        }
    )
    
    answer = response['output']['text']
    # print(f"$$$$$$$$$$$$$${answer}")
    citations = response.get('citations',[])

    return {'answers': answer, 'citations': citations}






