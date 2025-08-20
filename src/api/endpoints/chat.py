from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
import crud, schemas, models
from database import SessionLocal
from utils.llm_handler import generate_llm_response

router = APIRouter()

# Questo modulo gestisce le interazioni della chat con il modello LLM,
# consentendo agli utenti di interagire in diverse modalità (es. insegnante, compagno di conversazione, traduttore).



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/interaction", response_model=schemas.ChatMessage)
def chat_interaction(
    request: schemas.ChatInteractionRequest, db: Session = Depends(get_db)
):
    """
    Gestisce le interazioni della chat con il modello LLM in base alla modalità selezionata.
    NB. Guardare ChatInteractionRequest epr il body della richiesta
    """

    language = crud.get_language_by_name(db, request.language.capitalize())
    if not language:
        raise HTTPException(status_code=404, detail="Language not found")

    system_prompts = {
        "teacher": f"You are a {request.language} language teacher. Your role is to assist the user in learning {request.language}. Respond to their questions, correct their mistakes, and provide clear explanations in a supportive and encouraging manner.",
        "talk_buddy": f"You are a native {request.language} speaker and you are a friendly conversation partner for the user who is learning your language. Chat with them about various topics, ask questions, and help them practice their speaking skills in a natural and informal way.",
        "translator": f"You are a translation tool. Your task is to translate the user's text into {request.language}. Respond only with the translation of the user's message, without any additional comments or explanations.",
    }

    if request.mode not in system_prompts:
        raise HTTPException(
            status_code=400,
            detail="Invalid mode specified. Available modes: teacher, talk_buddy, translator.",
        )

    system_message = schemas.ChatMessage(
        role="system", content=system_prompts[request.mode]
    )

    full_message_history = [system_message] + request.messages

    prompt = "\n".join([f"{msg.role}: {msg.content}" for msg in full_message_history])

    try:
        llm_response_content = generate_llm_response(prompt)
        return schemas.ChatMessage(role="assistant", content=llm_response_content)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while communicating with the LLM: {e}",
        )


@router.get("/modes", response_model=List[str])
def get_available_modes():
    """
    Ritorna una lista delle modalità di interazione disponibili per la chat.
    """
    return ["teacher", "talk_buddy", "translator"]
