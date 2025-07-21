from pydantic import BaseModel, Field
from typing import Any, List, Optional
from langchain_core.runnables import RunnableConfig
import os
from enum import Enum

class SearchAPI(Enum):
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    TAVILY = "tavily"
    NONE = "none"

class MCPConfig(BaseModel):
    url: Optional[str] = Field(
        default=None,
        optional=True,
    )
    """The URL of the MCP server"""
    tools: Optional[List[str]] = Field(
        default=None,
        optional=True,
    )
    """The tools to make available to the LLM"""
    auth_required: Optional[bool] = Field(
        default=False,
        optional=True,
    )
    """Whether the MCP server requires authentication"""

class Configuration(BaseModel):
    # General Configuration
    max_structured_output_retries: int = Field(
        default=3,
        metadata={
            "x_oap_ui_config": {
                "type": "number",
                "default": 3,
                "min": 1,
                "max": 10,
                "description": "Maximum number of retries for structured output calls from models"
            }
        }
    )
    api_timeout_seconds: int = Field(
        default=60,
        metadata={
            "x_oap_ui_config": {
                "type": "number",
                "default": 60,
                "min": 10,
                "max": 300,
                "description": "Timeout in seconds for API calls to prevent hanging on malformed responses"
            }
        }
    )
    allow_clarification: bool = Field(
        default=True,
        metadata={
            "x_oap_ui_config": {
                "type": "boolean",
                "default": True,
                "description": "Whether to allow the researcher to ask the user clarifying questions before starting research"
            }
        }
    )
    max_concurrent_research_units: int = Field(
        default=5,
        metadata={
            "x_oap_ui_config": {
                "type": "slider",
                "default": 5,
                "min": 1,
                "max": 20,
                "step": 1,
                "description": "Maximum number of research units to run concurrently. This will allow the researcher to use multiple sub-agents to conduct research. Note: with more concurrency, you may run into rate limits."
            }
        }
    )
    # Research Configuration
    search_api: SearchAPI = Field(
        default=SearchAPI.TAVILY,
        metadata={
            "x_oap_ui_config": {
                "type": "select",
                "default": "tavily",
                "description": "Search API to use for research. NOTE: Make sure your Researcher Model supports the selected search API.",
                "options": [
                    {"label": "Tavily", "value": SearchAPI.TAVILY.value},
                    {"label": "OpenAI Native Web Search", "value": SearchAPI.OPENAI.value},
                    {"label": "Anthropic Native Web Search", "value": SearchAPI.ANTHROPIC.value},
                    {"label": "None", "value": SearchAPI.NONE.value}
                ]
            }
        }
    )
    max_researcher_iterations: int = Field(
        default=3,
        metadata={
            "x_oap_ui_config": {
                "type": "slider",
                "default": 3,
                "min": 1,
                "max": 10,
                "step": 1,
                "description": "Maximum number of research iterations for the Research Supervisor. This is the number of times the Research Supervisor will reflect on the research and ask follow-up questions."
            }
        }
    )
    max_react_tool_calls: int = Field(
        default=5,
        metadata={
            "x_oap_ui_config": {
                "type": "slider",
                "default": 5,
                "min": 1,
                "max": 30,
                "step": 1,
                "description": "Maximum number of tool calling iterations to make in a single researcher step."
            }
        }
    )
    # Model Configuration - Updated for Moonshot Models
    summarization_model: str = Field(
        default="openai:moonshot-v1-8k",
        metadata={
            "x_oap_ui_config": {
                "type": "text",
                "default": "openai:moonshot-v1-8k",
                "description": "Model for summarizing research results from Tavily search results. Using moonshot-v1-8k for efficient summarization."
            }
        }
    )
    summarization_model_max_tokens: int = Field(
        default=4000,
        metadata={
            "x_oap_ui_config": {
                "type": "number",
                "default": 4000,
                "description": "Maximum output tokens for summarization model (adjusted for moonshot-v1-8k)"
            }
        }
    )
    research_model: str = Field(
        default="openai:moonshot-v1-32k",
        metadata={
            "x_oap_ui_config": {
                "type": "text",
                "default": "openai:moonshot-v1-32k",
                "description": "Model for conducting research. Using moonshot-v1-32k for good context length and performance."
            }
        }
    )
    research_model_max_tokens: int = Field(
        default=8000,
        metadata={
            "x_oap_ui_config": {
                "type": "number",
                "default": 8000,
                "description": "Maximum output tokens for research model (adjusted for moonshot-v1-32k)"
            }
        }
    )
    compression_model: str = Field(
        default="openai:moonshot-v1-8k",
        metadata={
            "x_oap_ui_config": {
                "type": "text",
                "default": "openai:moonshot-v1-8k",
                "description": "Model for compressing research findings from sub-agents. Using moonshot-v1-8k for efficient compression."
            }
        }
    )
    compression_model_max_tokens: int = Field(
        default=4000,
        metadata={
            "x_oap_ui_config": {
                "type": "number",
                "default": 4000,
                "description": "Maximum output tokens for compression model (adjusted for moonshot-v1-8k)"
            }
        }
    )
    final_report_model: str = Field(
        default="openai:moonshot-v1-128k",
        metadata={
            "x_oap_ui_config": {
                "type": "text",
                "default": "openai:moonshot-v1-128k",
                "description": "Model for writing the final report from all research findings. Using moonshot-v1-128k for large context."
            }
        }
    )
    final_report_model_max_tokens: int = Field(
        default=16000,
        metadata={
            "x_oap_ui_config": {
                "type": "number",
                "default": 16000,
                "description": "Maximum output tokens for final report model (adjusted for moonshot-v1-128k)"
            }
        }
    )
    # MCP server configuration
    mcp_config: Optional[MCPConfig] = Field(
        default=None,
        optional=True,
        metadata={
            "x_oap_ui_config": {
                "type": "mcp",
                "description": "MCP server configuration"
            }
        }
    )
    mcp_prompt: Optional[str] = Field(
        default=None,
        optional=True,
        metadata={
            "x_oap_ui_config": {
                "type": "text",
                "description": "Any additional instructions to pass along to the Agent regarding the MCP tools that are available to it."
            }
        }
    )


    @classmethod
    def from_runnable_config(
        cls, config: Optional[RunnableConfig] = None
    ) -> "Configuration":
        """Create a Configuration instance from a RunnableConfig."""
        configurable = config.get("configurable", {}) if config else {}
        field_names = list(cls.model_fields.keys())
        values: dict[str, Any] = {
            field_name: os.environ.get(field_name.upper(), configurable.get(field_name))
            for field_name in field_names
        }
        return cls(**{k: v for k, v in values.items() if v is not None})

    class Config:
        arbitrary_types_allowed = True