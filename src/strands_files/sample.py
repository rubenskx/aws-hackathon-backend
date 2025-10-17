# from strands import Agent
# from my_strands_tools import kb_retriever

# agent = Agent(tools=[kb_retriever])

# def main():
#     result = agent("What are the compliance guidelines on cash flow statement?")
#     print(result)

# if __name__ == "__main__":
#     main()

# from strands import Agent
# from strands_tools.exa import exa_search, exa_get_contents

# agent = Agent(tools=[exa_search, exa_get_contents])

# # 1) Search
# def main():
#     search_res = agent.tool.exa_search(query="Acme Corp investor relations 2025", text=True)

#     # 2) Extract content from top result(s)
#     urls = [r.get("url") for r in search_res.get("results", [])][:3]
#     contents = agent.tool.exa_get_contents(urls=urls, text=True,
#         summary={"query": "key points about financials and management"})

#     print("Search results:", search_res)
#     print("Contents:", contents)


# if __name__ == "__main__":
#     main()


from strands import Agent
# Import the Tavily tools from strands_tools
from strands_tools.tavily import tavily_search, tavily_extract
from dotenv import load_dotenv

load_dotenv()

import re
import json
import ast

URL_RE = re.compile(r"https?://[^\s\"'<>]+", re.IGNORECASE)

def extract_urls_from_item(item):
    """Try to extract urls from a single item which may be dict or string."""
    urls = []

    # If dict, look for common fields
    if isinstance(item, dict):
        # common container keys that may hold results
        for key in ("results", "content", "items", "links"):
            val = item.get(key)
            if val:
                # if list, scan list elements
                if isinstance(val, list):
                    for sub in val:
                        urls += extract_urls_from_item(sub)
                elif isinstance(val, dict):
                    urls += extract_urls_from_item(val)
                elif isinstance(val, str):
                    # string may be JSON or Python repr
                    urls += extract_urls_from_item(val)
        # direct url-like fields
        for candidate_key in ("url", "URL", "link", "href", "uri"):
            v = item.get(candidate_key)
            if isinstance(v, str) and v.startswith("http"):
                urls.append(v)
        # sometimes entries have a 'text' field containing JSON-like structure
        if "text" in item and isinstance(item["text"], str):
            urls += extract_urls_from_item(item["text"])

    # If it's a string, try JSON -> literal_eval -> regex
    elif isinstance(item, str):
        txt = item.strip()
        # Try JSON
        try:
            parsed = json.loads(txt)
            urls += extract_urls_from_item(parsed)
        except Exception:
            # Try Python literal (single quotes etc)
            try:
                parsed = ast.literal_eval(txt)
                urls += extract_urls_from_item(parsed)
            except Exception:
                # Last resort: regex find urls in the text
                found = URL_RE.findall(txt)
                urls.extend(found)

    # If it's a list, iterate
    elif isinstance(item, list):
        for sub in item:
            urls += extract_urls_from_item(sub)

    # normalize and dedupe
    normalized = []
    for u in urls:
        if not isinstance(u, str):
            continue
        if u.endswith((".", ",", ";")):
            u = u[:-1]
        if u not in normalized:
            normalized.append(u)
    return normalized

def main():
    agent = Agent(tools=[tavily_search, tavily_extract])
    user_query = "What are the features of the strands-agents/tools GitHub repository and how to use Tavily with it?"

    # Step 1: Search
    search_res = agent.tool.tavily_search(query=user_query, search_depth="advanced")
    print("Search result type:", type(search_res))
    # small debug - show top-level keys or a truncated string
    if isinstance(search_res, dict):
        print("Top-level keys:", list(search_res.keys()))
    else:
        print("Search result (truncated):", str(search_res)[:1000])

    # Step 1.5: Extract URLs robustly
    urls = extract_urls_from_item(search_res)
    # As a safety, limit to unique and top 3
    urls = list(dict.fromkeys(urls))[:3]
    print("Extracting content from URLs:", urls)

    if not urls:
        print("No URLs found in search result — cannot call tavily_extract.")
        return

    # Step 2: Extract content
    extracted = agent.tool.tavily_extract(urls=urls, extract_depth="basic")
    print("Extracted content:", extracted)

    
if __name__ == "__main__":
    main()

