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

# Configuration
notebook_definitions = [
    "AEO_Lab_01_Concept",
    "AEO_Lab_02_Tech",
    "AEO_Lab_03_Biz"
]

sources_map = {
    "AEO_Lab_01_Concept": [
        "https://neilpatel.com/blog/answer-engine-optimization/",
        "https://cxl.com/blog/answer-engine-optimization/"
    ],
    "AEO_Lab_02_Tech": [
        "https://www.seoptimer.com/blog/faq-schema-markup/",
        "https://developers.google.com/search/docs/appearance/structured-data/faqpage"
    ],
    "AEO_Lab_03_Biz": [
        "https://neilpatel.com/blog/seo-audit-cost/",
        "https://agencyanalytics.com/blog/seo-pricing-guide"
    ]
}

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("🐟 Kodari Manager: Starting Restoration & Injection Mission...\n")

            # 1. Fetch Existing Notebooks
            print("🔍 Checking existing notebooks...")
            result = await session.call_tool("notebook_list", arguments={})
            existing_notebooks = {}
            try:
                data = json.loads(result.content[0].text)
                if isinstance(data, dict) and 'notebooks' in data:
                    items = data['notebooks']
                elif isinstance(data, list):
                    items = data
                else:
                    items = []
                
                for nb in items:
                    existing_notebooks[nb['title']] = nb['id']
            except Exception as e:
                print(f"❌ Error parsing list: {e}")
                return

            # 2. Create Missing Notebooks
            for title in notebook_definitions:
                if title in existing_notebooks:
                    print(f"✅ Found existing: '{title}' (ID: {existing_notebooks[title]})")
                else:
                    print(f"⚠️ Missing '{title}'. Creating now...")
                    try:
                        create_res = await session.call_tool("notebook_create", arguments={"title": title})
                        # Assume success returns the new notebook object or at least we re-list or try to parse
                        # Simpler: just try to parse result or wait
                        print(f"    ✅ Created '{title}'")
                        # We need the ID. List again? or parse create_res
                        # For robustness, let's just re-list after creation
                    except Exception as e:
                         print(f"    ❌ Failed to create '{title}': {e}")
            
            # Re-fetch list to get new IDs
            print("\n🔄 Refreshing notebook list for IDs...")
            result = await session.call_tool("notebook_list", arguments={})
            final_notebooks = {}
            try:
                data = json.loads(result.content[0].text)
                items = data.get('notebooks', []) if isinstance(data, dict) else (data if isinstance(data, list) else [])
                for nb in items:
                    final_notebooks[nb['title']] = nb['id']
            except:
                pass

            # 3. Inject Sources
            print("\n💉 Injecting Knowledge Sources...")
            for title, urls in sources_map.items():
                if title not in final_notebooks:
                    print(f"⚠️ Skip '{title}': Not found even after creation attempt.")
                    continue
                
                nb_id = final_notebooks[title]
                print(f"📂 Feeding '{title}'...")
                for url in urls:
                    print(f"  - Adding: {url}")
                    try:
                        await session.call_tool("notebook_add_url", arguments={"notebookId": nb_id, "url": url})
                    except Exception as e:
                        print(f"    ❌ Error: {e}")
            
            print("\n🎉 Mission Complete!")

if __name__ == "__main__":
    asyncio.run(run())
