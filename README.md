# 🐳 AgenticAI — Docker AI Agent with Ollama & MCP

A project that builds an **AI-powered Docker assistant** step by step — starting from a simple chatbot, adding tool-calling (agents), and finally connecting to an **MCP (Model Context Protocol) server** for a clean, scalable tool architecture.

All powered by **local LLMs via Ollama** — no OpenAI API key needed.

---

## 📁 Project Structure

```
AgenticAI/
│
├── generative_ai.py          # Step 1 — Simple chatbot (no tools)
├── agent.py                  # Step 2 — Agent with tools (local tools)
├── mcp_server.py             # Step 3a — MCP Server (exposes Docker tools)
├── agent_with_mcp(row).py    # Step 3b — Agent using MCP (single question)
├── agent_with_mcp.py         # Step 3c — Agent using MCP (full chat loop)
│
├── requirements.txt          # Python dependencies
└── README.md                 # You are here
```

---

## 🧠 What Does This Project Do?

It creates an AI assistant that can **talk to Docker** — asking it things like:

- *"How many containers are running?"*
- *"Show me the logs of my nginx container"*
- *"List all containers, including stopped ones"*

The AI reasons about your question, picks the right Docker tool, runs it, and explains the result in plain English — like a senior DevOps engineer you can chat with.

---

## 🔄 How It Works — Step by Step

### Step 1 — `generative_ai.py` : Simple Chatbot

> Just a basic AI chatbot. No tools, no Docker commands. Pure conversation.

```
You  →  "What does exit code 137 mean?"
AI   →  "It means the container was killed (OOM or manual stop)."
```

**How it works:**
- Uses the `ollama` Python package to talk to a local LLM (`gemma:2b`)
- Has a system prompt that tells the AI to act as a Docker expert
- Keeps a simple `while True` loop for conversation
- **No memory** between questions

---

### Step 2 — `agent.py` : Agent with Local Tools

> The AI can now actually **run Docker commands** on your machine.

```
You   →  "Show me running containers"
Agent →  [calls show_running_containers tool] → [runs: docker ps]
Agent →  "You have 3 containers running: nginx, redis, postgres"
```

**How it works:**
- Uses **LangChain** + **Ollama** to create a tool-calling agent
- Three tools are defined using `@tool` decorator:
  - `show_running_containers` → runs `docker ps`
  - `show_all_containers` → runs `docker ps -a`
  - `show_container_logs_by_name` → runs `docker logs <name>`
- The LLM **decides which tool to call** based on your question
- Uses `subprocess` to actually execute the Docker commands

---

### Step 3a — `mcp_server.py` : The MCP Server

> Takes the same Docker tools and **wraps them in an MCP server** — a standard protocol for AI tools.

**How it works:**
- Uses `FastMCP` to create a proper tool server
- Exposes the same 3 Docker tools (`show_running_containers`, `show_all_containers`, `show_container_logs_by_name`)
- Runs as a **separate process** that agents can connect to
- Any agent that speaks MCP can now use these tools — not just this project

Think of it like a **REST API for AI tools**.

---

### Step 3b — `agent_with_mcp(row).py` : Agent + MCP (Single Shot)

> Connects an agent to the MCP server and asks **one question**, then exits.

**How it works:**
- Uses `MultiServerMCPClient` from `langchain-mcp-adapters` to connect to the MCP server
- Starts `mcp_server.py` as a subprocess (via `stdio` transport)
- Fetches all available tools from the server automatically
- Runs one question and prints the answer

Good for **quick tests** to verify the MCP connection is working.

---

### Step 3c — `agent_with_mcp.py` : Agent + MCP (Full Chat Loop) ✅ Main File

> The **complete, production-ready version** — persistent chat with MCP tools and conversation memory.

```
User:  How many containers are running?
Agent: You have 2 containers running: nginx and redis.

User:  Show me the logs for nginx
Agent: [fetches logs] Here are the recent logs for nginx: ...

User:  exit
       Goodbye!
```

**How it works:**
- MCP client is initialized **once** (not reconnected every message — efficient)
- Maintains a `chat_history` list — the agent **remembers previous messages**
- Runs an infinite loop: takes input → sends full history to agent → prints response
- Handles errors gracefully with `try/except`
- Clean exit on `exit`, `quit`, or `bye`

---

## ⚙️ Installation

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.ai) installed and running locally
- Docker installed and running
- `gemma4` model pulled in Ollama:

```bash
ollama pull gemma4
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

**What each package does:**

| Package | Purpose |
|---|---|
| `ollama` | Connects Python to your local Ollama server |
| `langchain` | Framework for building AI agents |
| `langchain-ollama` | LangChain adapter for Ollama models |
| `langgraph` | Powers the agent's reasoning loop (think → act → observe) |
| `fastmcp` | Build and run MCP servers easily |
| `langchain-mcp-adapters` | Lets LangChain agents use MCP tools |

---

## 🚀 Running the Project

### Option A — Simple chatbot (no tools)
```bash
python generative_ai.py
```

### Option B — Agent with local tools
```bash
python agent.py
```

### Option C — Full agent with MCP *(recommended)*
```bash
python agent_with_mcp.py
```
> The agent automatically starts `mcp_server.py` in the background. You don't need to start it manually.

---

Without the comma, Python silently **concatenates** `"ps"` and `"-a"` into the string `"ps-a"`, and the command fails.

---

## 🏗️ Architecture Overview

```
┌─────────────┐        ┌──────────────────┐        ┌──────────────┐
│   You (CLI) │──────▶ │  LangChain Agent │──────▶ │  MCP Server  │
│             │        │  (gemma4 / Ollama)│        │ (mcp_server) │
└─────────────┘        └──────────────────┘        └──────┬───────┘
                                                          │
                                              ┌───────────▼──────────┐
                                              │   Docker CLI tools   │
                                              │  docker ps           │
                                              │  docker ps -a        │
                                              │  docker logs <name>  │
                                              └──────────────────────┘
```

---

## 💡 Ideas to Extend This Project

- Add more Docker tools: `docker stop`, `docker restart`, `docker inspect`
- Add a `docker stats` tool for live container resource usage
- Switch the model to `llama3`, `mistral`, or any other Ollama model
- Build a web UI using Streamlit or Gradio on top of the agent
- Deploy the MCP server over HTTP (instead of stdio) for remote access

---


