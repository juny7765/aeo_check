from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio
import os

# Define the server parameters
server_params = StdioServerParameters(
    command="C:\\Users\\ninja\\AppData\\Roaming\\Python\\Python313\\Scripts\\notebooklm-mcp.exe",
    args=[],
    env=os.environ
)

# Sources to inject
sources_map = {
    "AEO_Lab_01_Concept": [
        "https://neilpatel.com/blog/answer-engine-optimization/",
        "https://cxl.com/blog/answer-engine-optimization/",
        "https://ommdigitalsolution.com/answer-engine-optimization-aeo/"
    ],
    "AEO_Lab_02_Tech": [
        "https://developers.google.com/search/docs/appearance/structured-data/faqpage",
        "https://surferseo.com/blog/answer-engine-optimization/",
        "https://schemaapp.com/blog/schema-markup-for-answer-engine-optimization/"
    ],
    "AEO_Lab_03_Biz": [
        "https://relixir.ai/blog/aeo-answer-engine-optimization-pricing",
        "https://revenuezen.com/answer-engine-optimization-agencies/"
    ]
}

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # 1. Get List of Notebooks to find IDs
            print("🔍 Listing Notebooks to find IDs...")
            notebooks_result = await session.call_tool("notebook_list", arguments={})
            notebooks_text = notebooks_result.content[0].text
            
            import json
            print(f"DEBUG: Raw response type: {type(notebooks_text)}")
            print(f"DEBUG: Raw response prefix: {notebooks_text[:200]}...")

            try:
                data = json.loads(notebooks_text)
                print(f"DEBUG: Parsed JSON type: {type(data)}")
                
                if isinstance(data, dict) and 'notebooks' in data:
                    notebook_list = data['notebooks']
                elif isinstance(data, list):
                    notebook_list = data
                else:
                    print("⚠️ Unknown data structure. Treating as empty.")
                    notebook_list = []
                
                print(f"DEBUG: Notebook list length: {len(notebook_list)}")
                if len(notebook_list) > 0:
                    print(f"DEBUG: First item: {notebook_list[0]}")

            except Exception as e:
                print(f"❌ JSON Parsing Error: {e}")
                notebook_list = []

            # Map Titles to IDs
            title_to_id = {}
            for nb in notebook_list:
                if isinstance(nb, dict) and 'title' in nb and 'id' in nb:
                    title_to_id[nb['title']] = nb['id']
                else:
                    print(f"⚠️ Skipping invalid item: {nb}")

            print(f"✅ Found {len(title_to_id)} valid notebooks.")

            # 2. Inject Sources
            for title, urls in sources_map.items():
                if title not in title_to_id:
                    print(f"⚠️ Notebook '{title}' not found. Skipping.")
                    continue
                
                notebook_id = title_to_id[title]
                print(f"\n📂 Feeding '{title}' (ID: {notebook_id})...")
                
                for url in urls:
                    print(f"  - Adding URL: {url}")
                    try:
                        # Note: The actual tool name for adding a source might be 'source_add' or 'notebook_add_url'
                        # I'll try 'notebook_add_url' first as it follows the naming convention.
                        # If that fails, I'll try 'add_resource' or print available tools.
                        await session.call_tool("notebook_add_url", arguments={"notebookId": notebook_id, "url": url})
                        print("    ✅ Added!")
                    except Exception as e:
                        print(f"    ❌ Failed: {e}")

if __name__ == "__main__":
    asyncio.run(run())
