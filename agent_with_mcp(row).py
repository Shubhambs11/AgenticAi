import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
 

async def main():
    # this brings all the tools from mcp Server
    client = MultiServerMCPClient(
        {
            "docker-mcp": {
              "transport": "stdio",
              "command": "python.exe",
              "args": ["mcp_server.py"]
            }
        }
    )
    
    tools = await client.get_tools() # MCP Tools

    llm = ChatOllama(
    model="gemma4",
    temperature=0.8 ) #LLM

    # agent with MCP Tools
    agent = create_agent(
        llm,
        tools  
    )
    
    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "How many containers are running"}]}
    )

    print(response['messages'][-1].content)

if __name__ == "__main__":
    asyncio.run(main())