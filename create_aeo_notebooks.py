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

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Create the 3 AEO Notebooks
            notebooks_to_create = [
                "AEO_Lab_01_Concept",
                "AEO_Lab_02_Tech",
                "AEO_Lab_03_Biz"
            ]

            print(f"🐟 Kodari Manager: Starting Notebook Creation Mission...\\n")

            for title in notebooks_to_create:
                print(f"Creating notebook: {title}...")
                try:
                    result = await session.call_tool("notebook_create", arguments={"title": title})
                    print(f"✅ Success! Created '{title}'")
                    print(f"Details: {result.content}\\n")
                except Exception as e:
                    print(f"❌ Failed to create '{title}': {e}\\n")

if __name__ == "__main__":
    asyncio.run(run())
