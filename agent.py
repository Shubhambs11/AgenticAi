# Langchain
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain.agents import create_agent

# System package
import subprocess # package that can run commands on your terminal

SYSTEM_PROMPT = """
You are a Docker Expert. You can explain things in 1-2 lines max.
You don't overtink, hallucinate or keep resoning in loop.
You resone and act according to user prompt

there are the things you do:
1/ You tell about errors ( what went wrong, etc)
2/ Yor tell about the root cause ( what was cause likely)
3/ You tell about the fix or solution in short
"""

@tool
def show_running_containers():
    """Tool 1 : show Running Containers"""
    result = subprocess.run(["docker", "ps"], capture_output=True, text=True)
    return result.stdout 

@tool
def show_all_containers():
    """Tool 1 : show Running Containers"""
    result = subprocess.run(["docker", "ps", "-a"], capture_output=True, text=True)
    return result.stdout

@tool
def show_container_logs_by_name(container_name: str):
    """Tool 2 : show Container logs"""
    result = subprocess.run(["docker","logs",container_name], capture_output=True, text=True)
    return result.stdout 

llm = ChatOllama(
    model="gemma4",
    temperature="0.8",
    system= SYSTEM_PROMPT) #LLM
tools = [show_running_containers, show_container_logs_by_name, show_all_containers] # Tools

agent = create_agent(llm, tools)

while True:
    user_input = input("Enter your message:\n")
    if user_input == "exit":
        break
    response = agent.invoke({"messages" : [{
                    'role': 'user',
                    'content': user_input,
                }]})

    print(response['messages'][-1].content)