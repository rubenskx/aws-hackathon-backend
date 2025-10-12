from crewai_tools import PDFSearchTool
from dotenv import load_dotenv
load_dotenv()

rag_tool = PDFSearchTool(pdf='data/ind_as_1.pdf',
                         config=dict(
                             llm=dict(
                                 # or google, openai, anthropic, llama2, ...
                                 provider="openai",
                                 config=dict(
                                     model="gpt-5-nano",
                                     # temperature=0.5,
                                     # top_p=1,
                                     # stream=true,
                                 ),
                             ),
                             embedder=dict(
                                 # or openai, ollama, ...
                                 provider="openai",
                                 config=dict(
                                     model="text-embedding-3-small",
                                     # task_type="retrieval_document",
                                     # title="Embeddings",
                                 ),
                             ),
                         )
                         )
