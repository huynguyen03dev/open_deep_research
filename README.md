# Open Deep Research

<img width="1388" height="298" alt="full_diagram" src="https://github.com/user-attachments/assets/12a2371b-8be2-4219-9b48-90503eb43c69" />

Deep research has broken out as one of the most popular agent applications. This is a simple, configurable, fully open source deep research agent that works across many model providers, search tools, and MCP servers. 

* Read more in our [blog](https://blog.langchain.com/open-deep-research/) 
* See our [video](https://www.youtube.com/watch?v=agGiWUpxkhg) for a quick overview

### 🚀 Quickstart

1. Clone the repository and activate a virtual environment:
```bash
git clone https://github.com/langchain-ai/open_deep_research.git
cd open_deep_research
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
uv pip install -r pyproject.toml
```

3. Set up your `.env` file to customize the environment variables (for model selection, search tools, and other configuration settings):
```bash
cp .env.example .env
```

> **💡 Moonshot Integration**: For educational use with Moonshot models, see the [Moonshot Integration](#-moonshot-integration) section below for setup instructions using kimi-free-api.

4. Launch the assistant with the LangGraph server locally to open LangGraph Studio in your browser:

```bash
# Install dependencies and start the LangGraph server
uvx --refresh --from "langgraph-cli[inmem]" --with-editable . --python 3.11 langgraph dev --allow-blocking
```

Use this to open the Studio UI:
```
- 🚀 API: http://127.0.0.1:2024
- 🎨 Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
- 📚 API Docs: http://127.0.0.1:2024/docs
```
<img width="817" height="666" alt="Screenshot 2025-07-13 at 11 21 12 PM" src="https://github.com/user-attachments/assets/052f2ed3-c664-4a4f-8ec2-074349dcaa3f" />

Ask a question in the `messages` input field and click `Submit`.

### Configurations

Open Deep Research offers extensive configuration options to customize the research process and model behavior. All configurations can be set via the web UI, environment variables, or by modifying the configuration directly.

#### General Settings

- **Max Structured Output Retries** (default: 3): Maximum number of retries for structured output calls from models when parsing fails
- **Allow Clarification** (default: true): Whether to allow the researcher to ask clarifying questions before starting research
- **Max Concurrent Research Units** (default: 5): Maximum number of research units to run concurrently using sub-agents. Higher values enable faster research but may hit rate limits

#### Research Configuration

- **Search API** (default: Tavily): Choose from Tavily (works with all models), OpenAI Native Web Search, Anthropic Native Web Search, or None
- **Max Researcher Iterations** (default: 3): Number of times the Research Supervisor will reflect on research and ask follow-up questions
- **Max React Tool Calls** (default: 5): Maximum number of tool calling iterations in a single researcher step

#### Models

Open Deep Research uses multiple specialized models for different research tasks:

- **Summarization Model** (default: `openai:moonshot-v1-8k`): Summarizes research results from search APIs
- **Research Model** (default: `openai:moonshot-v1-32k`): Conducts research and analysis
- **Compression Model** (default: `openai:moonshot-v1-8k`): Compresses research findings from sub-agents
- **Final Report Model** (default: `openai:moonshot-v1-128k`): Writes the final comprehensive report

All models are configured using [init_chat_model() API](https://python.langchain.com/docs/how_to/chat_models_universal_init/) which supports providers like OpenAI, Anthropic, Google Vertex AI, and others.

**Important Model Requirements:**

1. **Structured Outputs**: All models must support structured outputs. Check support [here](https://python.langchain.com/docs/integrations/chat/).

2. **Search API Compatibility**: Research and Compression models must support your selected search API:
   - Anthropic search requires Anthropic models with web search capability
   - OpenAI search requires OpenAI models with web search capability  
   - Tavily works with all models

3. **Tool Calling**: All models must support tool calling functionality

4. **Special Configurations**:
   - For OpenRouter: Follow [this guide](https://github.com/langchain-ai/open_deep_research/issues/75#issuecomment-2811472408)
   - For local models via Ollama: See [setup instructions](https://github.com/langchain-ai/open_deep_research/issues/65#issuecomment-2743586318)

### 🌙 Moonshot Integration

> **⚠️ EDUCATIONAL DISCLAIMER**: The Moonshot integration using kimi-free-api is provided for **educational and research purposes only**. Users must comply with all applicable terms of service, legal requirements, and usage policies. This integration is not intended for commercial use or production environments. Please ensure you have proper authorization and comply with all relevant terms of service before using this integration.

Open Deep Research now supports integration with Moonshot models via the [kimi-free-api](https://github.com/LLM-Red-Team/kimi-free-api/) project, which provides an OpenAI-compatible API interface for Moonshot models.

#### Available Moonshot Models

The application supports the following Moonshot models:

- **moonshot-v1**: Base model for general tasks
- **moonshot-v1-8k**: 8K context model (efficient for summarization and compression)
- **moonshot-v1-32k**: 32K context model (ideal for research tasks)
- **moonshot-v1-128k**: 128K context model (best for comprehensive final reports)
- **moonshot-v1-vision**: Vision-capable model
- **kimi-k2-0711-preview**: Preview model with advanced capabilities

#### Default Moonshot Configuration

The application is pre-configured with optimized Moonshot models for each task:

| Task | Model | Context | Purpose |
|------|-------|---------|---------|
| **Research** | `moonshot-v1-32k` | 32K tokens | Complex research and analysis |
| **Summarization** | `moonshot-v1-8k` | 8K tokens | Efficient search result summaries |
| **Compression** | `moonshot-v1-8k` | 8K tokens | Research findings compression |
| **Final Reports** | `moonshot-v1-128k` | 128K tokens | Comprehensive report generation |

#### Setup Instructions

**1. Set up kimi-free-api Server**

First, set up the kimi-free-api server to provide an OpenAI-compatible interface:

```bash
# Clone and set up kimi-free-api (follow their documentation)
git clone https://github.com/LLM-Red-Team/kimi-free-api.git
cd kimi-free-api
# Follow the setup instructions in their README
# Start the server on localhost:8010
```

**2. Configure Environment Variables**

Update your `.env` file with the following configuration:

```bash
# Moonshot API Configuration (via kimi-free-api)
OPENAI_API_KEY=your-moonshot-api-key-here
OPENAI_API_BASE=http://localhost:8010/v1

# Search API (required for research functionality)
TAVILY_API_KEY=your-tavily-api-key-here

# Optional: Other providers (leave empty for Moonshot-only setup)
ANTHROPIC_API_KEY=
GOOGLE_API_KEY=

# LangSmith (optional for tracing)
LANGSMITH_API_KEY=
LANGSMITH_PROJECT=moonshot-research
LANGSMITH_TRACING=false

# Configuration source
GET_API_KEYS_FROM_CONFIG=false
```

**3. Start the Application**

```bash
# Start the LangGraph server
uvx --refresh --from "langgraph-cli[inmem]" --with-editable . --python 3.11 langgraph dev --allow-blocking
```

#### Troubleshooting

**Common Issues and Solutions:**

1. **JSON Parsing Errors**
   - **Issue**: "ValueError: expected value at line 1 column 1"
   - **Solution**: The application includes robust fallback mechanisms that automatically handle JSON parsing issues with local APIs

2. **Model Not Found Errors**
   - **Issue**: "服务内部错误" (Internal service error)
   - **Solution**: Ensure your kimi-free-api server supports the specific Moonshot model and is running on the correct port

3. **Connection Errors**
   - **Issue**: Cannot connect to localhost:8010
   - **Solution**: Verify the kimi-free-api server is running and accessible on the specified port

4. **API Key Issues**
   - **Issue**: Authentication failures
   - **Solution**: Ensure your Moonshot API key is valid and properly configured in the kimi-free-api server

**Monitoring Model Usage:**

Check your server logs to confirm Moonshot models are being used:

```
✅ Good: [info] 使用模型: moonshot-v1-32k
❌ Bad:  [error] 使用模型: gpt-4.1
```

#### Educational Use Guidelines

When using this integration for educational purposes:

1. **Respect Terms of Service**: Ensure compliance with all applicable terms of service
2. **Rate Limiting**: Be mindful of API rate limits and usage quotas
3. **Data Privacy**: Do not process sensitive or confidential information
4. **Academic Use**: Ideal for research projects, learning, and educational demonstrations
5. **Responsible Usage**: Use responsibly and ethically in accordance with all applicable policies

#### Example MCP (Model Context Protocol) Servers

Open Deep Research supports MCP servers to extend research capabilities. 

#### Local MCP Servers

**Filesystem MCP Server** provides secure file system operations with robust access control:
- Read, write, and manage files and directories
- Perform operations like reading file contents, creating directories, moving files, and searching
- Restrict operations to predefined directories for security
- Support for both command-line configuration and dynamic MCP roots

Example usage:
```bash
mcp-server-filesystem /path/to/allowed/dir1 /path/to/allowed/dir2
```

#### Remote MCP Servers  

**Remote MCP servers** enable distributed agent coordination and support streamable HTTP requests. Unlike local servers, they can be multi-tenant and require more complex authentication.

**Arcade MCP Server Example**:
```json
{
  "url": "https://api.arcade.dev/v1/mcps/ms_0ujssxh0cECutqzMgbtXSGnjorm",
  "tools": ["Search_SearchHotels", "Search_SearchOneWayFlights", "Search_SearchRoundtripFlights"]
}
```

Remote servers can be configured as authenticated or unauthenticated and support JWT-based authentication through OAuth endpoints.

### Evaluation

A comprehensive batch evaluation system designed for detailed analysis and comparative studies.

#### **Features:**
- **Multi-dimensional Scoring**: Specialized evaluators with 0-1 scale ratings
- **Dataset-driven Evaluation**: Batch processing across multiple test cases

#### **Usage:**
```bash
# Run comprehensive evaluation on LangSmith datasets
python tests/run_evaluate.py
```
#### **Key Files:**
- `tests/run_evaluate.py`: Main evaluation script
- `tests/evaluators.py`: Specialized evaluator functions
- `tests/prompts.py`: Evaluation prompts for each dimension

### Deployments and Usages

#### LangGraph Studio

Follow the [quickstart](#-quickstart) to start LangGraph server locally and test the agent out on LangGraph Studio.

#### Hosted deployment
 
You can easily deploy to [LangGraph Platform](https://langchain-ai.github.io/langgraph/concepts/#deployment-options). 

#### Open Agent Platform

Open Agent Platform (OAP) is a UI from which non-technical users can build and configure their own agents. OAP is great for allowing users to configure the Deep Researcher with different MCP tools and search APIs that are best suited to their needs and the problems that they want to solve.

We've deployed Open Deep Research to our public demo instance of OAP. All you need to do is add your API Keys, and you can test out the Deep Researcher for yourself! Try it out [here](https://oap.langchain.com)

You can also deploy your own instance of OAP, and make your own custom agents (like Deep Researcher) available on it to your users.
1. [Deploy Open Agent Platform](https://docs.oap.langchain.com/quickstart)
2. [Add Deep Researcher to OAP](https://docs.oap.langchain.com/setup/agents)

### Updates 🔥

### Legacy Implementations 🏛️

The `src/legacy/` folder contains two earlier implementations that provide alternative approaches to automated research:

#### 1. Workflow Implementation (`legacy/graph.py`)
- **Plan-and-Execute**: Structured workflow with human-in-the-loop planning
- **Sequential Processing**: Creates sections one by one with reflection
- **Interactive Control**: Allows feedback and approval of report plans
- **Quality Focused**: Emphasizes accuracy through iterative refinement

#### 2. Multi-Agent Implementation (`legacy/multi_agent.py`)  
- **Supervisor-Researcher Architecture**: Coordinated multi-agent system
- **Parallel Processing**: Multiple researchers work simultaneously
- **Speed Optimized**: Faster report generation through concurrency
- **MCP Support**: Extensive Model Context Protocol integration

See `src/legacy/legacy.md` for detailed documentation, configuration options, and usage examples for both legacy implementations.
