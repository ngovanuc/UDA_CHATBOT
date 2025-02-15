import os
from typing import List, Optional, Union

from loguru import logger
from uac.configs.config import Config
from uac.llms.groq_client import GroqClient
from uac.llms.ollama_client import OllamaClient
from uac.llms.openai_client import OpenAIClient


# Initialize clients with configuration
config = Config()
ollama = OllamaClient(config)
openai = OpenAIClient(
    config, host=os.environ["OPENAI_BASE_URL"], api_key=os.environ["OPENAI_API_KEY"]
)
groq = GroqClient(config)

# All supported models categorized by backend
all_models = {
    "GROQ": [
        ("LLAMA3 8B", "llama3-8b-8192"),
        ("LLAMA3 70B", "llama3-70b-8192"),
        ("LLAMA3.1 70B", "llama-3.1-70b-versatile"),
        ("LLAMA3.1 8B", "llama-3.1-8b-instant"),
        ("LLAMA3.3 70B", "llama-3.3-70b-specdec"),
        ("LLAMA2 70B", "llama2-70b-4096"),
        ("Mixtral", "mixtral-8x7b-32768"),
        ("GEMMA 7B", "gemma-7b-it"),

    ],
    "OPENAI": [("4O-MINI", "gpt-4o-mini")],
    "LOCAL_AI": [
        ("QWEN2.5 3B GGUF", "Qwen2.5-3B-Instruct-GGUF-Q6-K"),
        ("QWEN2.5 7B GGUF", "Qwen2.5-7B-Instruct-GGUF-Q6-K"),
        ("Qwen2.5 72B GGUF", "Qwen2.5-72B-Instruct-GGUF-Q5-K-M"),
        ("QWEN2.5 3B GPTQ", "Qwen2.5-3B-Instruct-GPTQ-Int4"),
        ("QWEN2.5 7B GPTQ", "Qwen2.5-7B-Instruct-GPTQ-Int4"),
        ("Qwen2.5 72B GPTQ", "Qwen2.5-72B-Instruct-GPTQ-Int4"),
        ("Qwen2.5 72B AWQ", "Qwen2.5-72B-Instruct-AWQ"),
    ],
    "OLLAMA": [],
}

# Populate OLLAMA models if the client is available
if ollama.client:
    all_models["OLLAMA"] = ollama.models


def model_id_to_backend(model_name: str) -> Optional[str]:
    """
    Determines the backend corresponding to a given model identifier.

    Args:
        model_name (str): The identifier of the model.

    Returns:
        Optional[str]: The name of the backend supporting the model if found; otherwise, None.

    Example:
        >>> backend = model_id_to_backend("llama3-8b-8192")
        >>> print(backend)
        "GROQ"
    """
    for backend, models in all_models.items():
        for model in models:
            if model[1] == model_name:
                return backend
    return None


class LLM:
    """
    A class for managing and interfacing with various Large Language Models (LLMs).

    Attributes:
        model_id (str): The identifier for the model to be used.
    """

    def __init__(self, model_id: Optional[str] = None):
        """
        Initializes the LLM class with an optional model ID.

        Args:
            model_id (Optional[str], optional): The identifier for the model to be used. Defaults to None.
        """
        self.model_id = model_id

    def list_models(self) -> dict:
        """
        Retrieves a dictionary of all supported models categorized by their backends.

        Returns:
            dict: A dictionary where keys are backend names and values are lists of tuples
                  containing model names and their corresponding identifiers.

        Example:
            >>> models = llm.list_models()
            >>> print(models["GROQ"])
            [("LLAMA3 8B", "llama3-8b-8192"), ...]
        """
        return all_models

    def get_model_client(self) -> Union[GroqClient, OpenAIClient, OllamaClient]:
        """
        Retrieves the client instance corresponding to the model's backend.

        Returns:
            Union[GroqClient, OpenAIClient, OllamaClient]: The client instance for the model's backend.

        Raises:
            ValueError: If the model ID is not supported or if the backend for the model ID is not found.

        Example:
            >>> client = llm.get_model_client()
            >>> response = client.client_response("Hello")
        """
        model_backend = model_id_to_backend(self.model_id)
        if model_backend is None:
            raise ValueError(f"Model '{self.model_id}' is not supported.")
        logger.success(f"Model: {self.model_id}, Backend: {model_backend}")

        model_mapping = {"OLLAMA": ollama, "OPENAI": openai, "GROQ": groq}

        try:
            model_client = model_mapping[model_backend]
            return model_client
        except KeyError:
            raise ValueError(f"Backend '{model_backend}' is not supported.")

    def client_response(self, messages: List[dict], max_tokens: int = 1024, **kwargs) -> str:
        """
        Generates a synchronous response from the specified model based on input messages.

        Args:
            messages (List[dict]): A list of input messages to be processed by the model.
            max_tokens (int, optional): The maximum number of tokens in the response. Defaults to 1024.
            **kwargs: Additional keyword arguments for the model client.

        Returns:
            str: The response generated by the model based on the input messages.

        Example:
            >>> response = llm.client_response([
            ...     {"role": "user", "content": "Hello, how are you?"}
            ... ])
            >>> print(response)
            "I'm fine, thank you! How can I assist you today?"
        """
        model_client = self.get_model_client()
        response = model_client.client_response(
            self.model_id, messages, max_tokens=max_tokens, **kwargs
        )
        return response

    async def aclient_response(
        self,
        messages: List[dict],
        max_tokens: int = 1024,
        temperature: float = 0.1,
        **kwargs,
    ) -> str:
        """
        Asynchronously generates a response from the specified model based on input messages.

        Args:
            messages (List[dict]): A list of input messages to be processed by the model.
            max_tokens (int, optional): The maximum number of tokens in the response. Defaults to 1024.
            temperature (float, optional): Sampling temperature for response generation. Defaults to 0.1.
            **kwargs: Additional keyword arguments for the model client.

        Returns:
            str: The response generated by the model based on the input messages.

        Example:
            >>> response = await llm.aclient_response([
            ...     {"role": "user", "content": "Tell me a joke."}
            ... ])
            >>> print(response)
            "Why did the scarecrow win an award? Because he was outstanding in his field!"
        """
        model_client = self.get_model_client()
        response = await model_client.aclient_response(
            self.model_id, messages, max_tokens=max_tokens, temperature=temperature, **kwargs
        )
        return response

    async def toolcall_response(
        self,
        messages: List[dict],
        max_tokens: int = 1024,
        tools: Optional[List] = None,
        tool_choice: Optional[str] = None,
    ) -> str:
        """
        Asynchronously generates a response from the specified model using tool calls.

        Args:
            messages (List[dict]): A list of input messages to be processed by the model.
            max_tokens (int, optional): The maximum number of tokens in the response. Defaults to 1024.
            tools (Optional[List], optional): A list of tools available for the model to use. Defaults to None.
            tool_choice (Optional[str], optional): A specific tool choice for the model to use. Defaults to None.

        Returns:
            str: The response generated by the model based on the input messages.

        Example:
            >>> response = await llm.toolcall_response(
            ...     messages=[{"role": "user", "content": "Analyze this data."}],
            ...     tools=["tool1", "tool2"],
            ...     tool_choice="tool1"
            ... )
            >>> print(response)
            "Data analysis complete using tool1."
        """
        model_client = self.get_model_client()
        response = await model_client.toolcall_response(
            self.model_id,
            messages,
            max_tokens=max_tokens,
            tools=tools,
            tool_choice=tool_choice,
        )
        return response
