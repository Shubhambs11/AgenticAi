from fastmcp import FastMCP
import subprocess

mcp = FastMCP("Docker MCP Server") # instace

@mcp.tool
def show_running_containers():
    """Tool 1 : show Running Containers"""
    result = subprocess.run(["docker", "ps"], capture_output=True, text=True)
    return result.stdout 

@mcp.tool
def show_all_containers():
    """Tool 1 : show Running Containers"""
    result = subprocess.run(["docker", "ps" "-a"], capture_output=True, text=True)
    return result.stdout

@mcp.tool
def show_container_logs_by_name(container_name: str):
    """Tool 2 : show Container logs"""
    result = subprocess.run(["docker","logs",container_name], capture_output=True, text=True)
    return result.stdout 


if __name__ == "__main__":
    mcp.run()