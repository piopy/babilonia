import os
import google.generativeai as genai
from dotenv import load_dotenv
from ast import literal_eval

load_dotenv()

# TODO l'API KEY può essere volendo inserita a db cifrata o inviata ad ogni richiesta
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=api_key)

generation_config = {
    "temperature": 0.8,  
    "top_p": 1.0,
    "top_k": 1,
    "max_output_tokens": 2048,
}

# Blocco contenuti poco carini
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

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-flash-latest")

model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    generation_config=generation_config,
    safety_settings=safety_settings,
)


def generate_llm_response(prompt: str) -> str:
    """
    Genera una risposta dal modello linguistico di Gemini basata su un prompt fornito.
    
    Args:
        prompt: Il prompt da inviare al modello linguistico.

    Returns:
        La risposta testuale dal modello linguistico.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return "Error: Could not get a response from the language model."


def clean_json_response(response: str) -> str:
    """
    Pulisce la risposta JSON dal modello LLM rimuovendo i marcatori del blocco di codice.

    Args:
        response: La risposta JSON grezza dal modello LLM.

    Returns:
        La risposta JSON pulita.
    """
    return literal_eval(response.replace("```json", "").replace("```", ""))
