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
            print("🔍 Fetching Notebook List...")
            result = await session.call_tool("notebook_list", arguments={})
            print(f"DEBUG RAW RESPONSE: {result.content}")
            try:
                data = json.loads(result.content[0].text)
                notebooks = data.get('notebooks', []) if isinstance(data, dict) else data
                
                print(f"✅ Found {len(notebooks)} notebooks:")
                for nb in notebooks:
                    title = nb.get('title', 'Unknown')
                    print(f" - [{title}] (ID: {nb.get('id', 'N/A')})")
            except Exception as e:
                print(f"❌ Error parsing list: {e}")
                print(f"Raw content: {result.content[0].text[:500]}")

if __name__ == "__main__":
    asyncio.run(run())
