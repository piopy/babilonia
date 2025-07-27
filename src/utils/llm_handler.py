import os
import google.generativeai as genai
from dotenv import load_dotenv
from ast import literal_eval

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=api_key)

# Configuration for the generative model
generation_config = {
    "temperature": 0.8,  # More creative
    "top_p": 1.0,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]

# Get model name from environment variable, with a default
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-flash-latest")

model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    generation_config=generation_config,
    safety_settings=safety_settings,
)


def generate_llm_response(prompt: str) -> str:
    """
    Generates a response from the Gemini LLM based on a given prompt.

    Args:
        prompt: The prompt to send to the LLM.

    Returns:
        The text response from the LLM.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Basic error handling, can be improved with more specific logging
        print(f"Error calling Gemini API: {e}")
        return "Error: Could not get a response from the language model."


def clean_json_response(response: str) -> str:
    """
    Cleans the JSON response from the LLM by removing code block markers.

    Args:
        response: The raw JSON response from the LLM.

    Returns:
        The cleaned JSON response.
    """
    return literal_eval(response.replace("```json", "").replace("```", ""))
