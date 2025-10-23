import boto3
import json
from dotenv import load_dotenv
load_dotenv()

bedrock_agent_runtime = boto3.client(
    service_name='bedrock-agent-runtime',
    region_name='us-east-1'  # e.g., 'us-east-1', 'us-west-2'
)


def retrieve_and_generate(knowledge_base_id, query, model_id):
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

    return response

if __name__=="__main__":
    knowledge_base_id = 'O3IBGYPABF'
    query = 'What information do you have about compliance guidelines on cash flow statement?'
    model_id = 'arn:aws:bedrock:us-east-1:992382746523:inference-profile/us.anthropic.claude-3-7-sonnet-20250219-v1:0'

    try:
        result = retrieve_and_generate(knowledge_base_id, query, model_id)

        # Extract the generated answer
        answer = result['output']['text']
        print(f"Answer: {answer}")

        # Retrieve citation information
        citations = result.get('citations', [])
        for citation in citations:
            print(f"Citation: {citation}")

    except Exception as e:
        print(f"Error: {str(e)}")