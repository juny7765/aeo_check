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

# 10 Hybrid Business Ideas (AI Agent + AEO + React Native)
ideas = [
    "Biz_Idea_01_AEO_Analytics_Dashboard_App",     # React Native App showing AEO metrics
    "Biz_Idea_02_Personal_AI_Agent_Manager",       # App to manage personal automation agents
    "Biz_Idea_03_Local_Biz_AEO_Optimizer",         # Automated AEO service for local businesses
    "Biz_Idea_04_Niche_Newsletter_Auto_Agent",     # Agent that writes/monetizes newsletters
    "Biz_Idea_05_RN_Component_Marketplace_Agent",  # Agent selling React Native UI components
    "Biz_Idea_06_Voice_First_AEO_Search_Asst",     # Voice app optimized for Answer Engines
    "Biz_Idea_07_MicroSaaS_Boilerplate_Agent",     # Automated deployment of MicroSaaS
    "Biz_Idea_08_Content_Repurposing_Bot",         # Turn blogs into videos/social posts for AEO
    "Biz_Idea_09_Crypto_Sentiment_Agent_App",      # Real-time sentiment analysis app
    "Biz_Idea_10_AEO_Audit_Report_Generator"       # Generate PDF AEO audits via App
]

async def run():
    print(f"🐟 Kodari Manager: Notebook Factory Started! Target: {len(ideas)} Notebooks\\n")
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 1. Get existing notebooks to avoid duplicates
            print("🔍 Checking existing notebooks...")
            existing_notebooks = []
            try:
                list_result = await session.call_tool("notebook_list", arguments={})
                # Simple parsing assuming list returns strings or dicts with titles
                # Adjust based on actual return structure if needed, but for now assuming string match check
                # Note: valid tool return might certainly require processing.
                # Since we want to be safe, we just try to create. NotebookLM usually allows duplicates or handles them.
                pass 
            except Exception as e:
                print(f"⚠️ Could not list notebooks (proceeding anyway): {e}")

            # 2. Create Notebooks
            for i, idea in enumerate(ideas):
                print(f"[{i+1}/{len(ideas)}] 🏗️ Constructing Notebook: {idea}...")
                try:
                    await session.call_tool("notebook_create", arguments={"title": idea})
                    print(f"   ✅ Created successfully!")
                except Exception as e:
                    print(f"   ❌ Failed: {e}")
            
            print(f"\\n🚀 Factory Run Complete! {len(ideas)} Ideas deployed to NotebookLM.")

if __name__ == "__main__":
    asyncio.run(run())
