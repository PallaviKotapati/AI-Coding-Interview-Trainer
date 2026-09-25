import requests
import json
import logging
from typing import Optional
from config import OLLAMA_BASE_URL, OLLAMA_GENERATE_ENDPOINT, DEFAULT_MODEL, LLM_TIMEOUT

logger = logging.getLogger(__name__)

class OllamaConnectionError(Exception):
    """Raised when communication with the local Ollama instance fails."""
    pass

class OllamaInferenceError(Exception):
    """Raised when Ollama returns an error status during inference."""
    pass

def check_connection() -> bool:
    """
    Checks if the local Ollama server is running and accessible.
    
    Returns:
        bool: True if Ollama is reachable, False otherwise.
    """
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=3)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def generate_response(
    prompt: str,
    system_prompt: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: Optional[int] = 400,
    model: Optional[str] = None,
    timeout: Optional[int] = None
) -> str:
    """
    Sends a generation request to the local Ollama API for Mistral.

    Args:
        prompt (str): The user/instruction prompt to send.
        system_prompt (Optional[str]): Optional system role instruction.
        temperature (float): Sampling temperature (0.0 = deterministic, 1.0 = creative).
        model (Optional[str]): Model name, defaults to config.DEFAULT_MODEL.
        timeout (Optional[int]): Request timeout in seconds, defaults to config.LLM_TIMEOUT.

    Returns:
        str: Generated text from the LLM.

    Raises:
        OllamaConnectionError: If the Ollama server is unreachable or timed out.
        OllamaInferenceError: If Ollama reports an inference or model error.
    """
    target_model = model or DEFAULT_MODEL
    req_timeout = timeout or LLM_TIMEOUT

    payload = {
        "model": target_model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": max(0.0, min(1.0, temperature)),
            "num_predict": max_tokens or 400
        }
    }

    if system_prompt:
        payload["system"] = system_prompt

    try:
        response = requests.post(
            OLLAMA_GENERATE_ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=req_timeout
        )
    except requests.exceptions.Timeout:
        logger.error(f"Ollama request timed out after {req_timeout} seconds.")
        raise OllamaConnectionError(
            f"Ollama request timed out after {req_timeout}s. The local model might be under heavy load."
        )
    except requests.exceptions.ConnectionError:
        logger.error(f"Failed to connect to Ollama at {OLLAMA_GENERATE_ENDPOINT}.")
        raise OllamaConnectionError(
            f"Could not connect to Ollama at {OLLAMA_BASE_URL}. "
            "Please ensure the Ollama service is running ('ollama serve' or active in system tray)."
        )
    except requests.exceptions.RequestException as exc:
        logger.error(f"Unexpected network error when calling Ollama: {exc}")
        raise OllamaConnectionError(f"Network error communicating with Ollama: {exc}")

    if response.status_code != 200:
        logger.error(f"Ollama API returned HTTP {response.status_code}: {response.text}")
        raise OllamaInferenceError(
            f"Ollama returned HTTP {response.status_code}: {response.text}"
        )

    try:
        result = response.json()
        return result.get("response", "").strip()
    except json.JSONDecodeError:
        logger.error("Failed to parse JSON response from Ollama API.")
        raise OllamaInferenceError("Invalid JSON received from Ollama API.")
