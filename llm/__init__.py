"""LLM Module for interacting with local Ollama instance."""
from .ollama_client import generate_response, check_connection

__all__ = ["generate_response", "check_connection"]
