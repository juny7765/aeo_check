from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio
import os
import json

server_params = StdioServerParameters(
    command="C:\\Users\\ninja\\AppData\\Roaming\\Python\\Python313\\Scripts\\notebooklm-mcp.exe",
    args=[],
    env=os.environ
)

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # 1. Find the Concept Notebook ID
            print("🔍 Locating 'AEO_Lab_01_Concept'...")
            result = await session.call_tool("notebook_list", arguments={})
            notebook_id = None
            try:
                data = json.loads(result.content[0].text)
                items = data.get('notebooks', []) if isinstance(data, dict) else (data if isinstance(data, list) else [])
                for nb in items:
                    if nb['title'] == "AEO_Lab_01_Concept":
                        notebook_id = nb['id']
                        break
            except:
                pass

            if not notebook_id:
                print("❌ Could not find the notebook. Creation might have failed.")
                return

            print(f"✅ Found Notebook ID: {notebook_id}")

            # 2. Ask a Question
            question = "Explain what AEO is and why it is important for 2024. Summarize based on the sources."
            print(f"\n❓ Asking: '{question}'...\n")
            
            # Note: The tool name generally follows the pattern. 
            # If 'notebook_query' isn't the name, we check 'query' or similar. 
            # Based on standard MCP mapping, it should be 'notebook_query'.
            try:
                # Some implementations use 'query' as argument, some 'text'. 
                # We'll try 'query' first based on common patterns.
                # Adjusting to likely schema: query(notebookId, query)
                response = await session.call_tool("notebook_query", arguments={"notebookId": notebook_id, "query": question})
                
                print("💡 NotebookLM Answer:")
                print("--------------------------------------------------")
                print(response.content[0].text)
                print("--------------------------------------------------")
            except Exception as e:
                print(f"❌ Query failed: {e}")

if __name__ == "__main__":
    asyncio.run(run())
