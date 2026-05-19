"""MiMo V2.5 API client for AgentGuard."""

import os
from dataclasses import dataclass, field


@dataclass
class MiMoConfig:
    api_key: str = ""
    base_url: str = "https://api.xiaomimimo.com/v1"
    model: str = "mimo-v2.5-pro"
    temperature: float = 0.1
    max_tokens: int = 4096

    def __post_init__(self):
        if not self.api_key:
            self.api_key = os.environ.get("MIMO_API_KEY", "")


class MiMoClient:
    """HTTP client for MiMo V2.5 API."""

    def __init__(self, config=None):
        self.config = config or MiMoConfig()
        self.chat = ChatCompletions(self.config)


class ChatCompletions:
    def __init__(self, config):
        self.config = config

    def create(self, model, messages, **kwargs):
        """Create a chat completion."""
        import httpx
        response = httpx.post(
            f"{self.config.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.config.api_key}"},
            json={
                "model": model,
                "messages": messages,
                "temperature": kwargs.get("temperature", self.config.temperature),
                "max_tokens": kwargs.get("max_tokens", self.config.max_tokens),
            },
            timeout=120,
        )
        response.raise_for_status()
        data = response.json()
        return ChatCompletion(**data)


@dataclass
class Message:
    content: str = ""
    role: str = "assistant"


@dataclass
class Choice:
    message: Message = field(default_factory=Message)


@dataclass
class ChatCompletion:
    choices: list = field(default_factory=list)

    def __post_init__(self):
        if self.choices and isinstance(self.choices[0], dict):
            self.choices = [Choice(message=Message(**c.get("message", {}))) for c in self.choices]
