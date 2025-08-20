from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import schemas, crud, models
from database import SessionLocal
from utils.llm_handler import generate_llm_response, clean_json_response
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
import os
import json
from typing import List, Optional

router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


@router.get("/exercises/daily-practice")
def get_daily_practice(
    target_language: str, current_user: models.User = Depends(get_current_user)
):
    """
    Genera una serie di 5 frasi semplici e di vita quotidiana per esercitarsi.
    """
    prompt = f"""Create a set of 5 simple, daily-life sentences in {target_language} for a beginner learner. The user's native language is {current_user.native_language}. For each sentence, provide the sentence in the target language, and its translation in the user's native language. Format the output as a JSON array of objects, where each object has 'sentence' and 'translation' keys."""

    response = generate_llm_response(prompt)
    return {"practice_sentences": clean_json_response(response)}


@router.get("/exercises/daily-quote")
def get_daily_quote(
    target_language: str, current_user: models.User = Depends(get_current_user)
):
    """
    Ritorna una citazione giornaliero in un certo linguaggio.
    """
    prompt = f"""Name a famous quote translated into the {target_language} language, with "<translated_{target_language}_quote> / <translated_{current_user.native_language}_quote> - (<author>)" style. Format the output just with the quote text and the author, without any other text. The translation must be in the {current_user.native_language} language."""

    response = generate_llm_response(prompt)
    return {"quote": response}


@router.get("/exercises/fill-in-the-blank")
def get_fill_in_the_blank_exercise(
    target_language: str,
    current_user: models.User = Depends(get_current_user),
    topic: Optional[str] = None,
    lesson_focus: Optional[str] = None,
):
    """
    Crea un esercizio "riempi gli spazi" basato su un argomento o un focus grammaticale.
    """
    prompt_parts = [
        f"Create a 'fill-in-the-blank' exercise for a beginner learning {target_language}.",
        f"The user's native language is {current_user.native_language}.",
        f"The exercise must be in the {target_language} language.",
    ]
    if topic:
        prompt_parts.append(f"The topic should be about: {topic}.")
    if lesson_focus:
        prompt_parts.append(
            f"The exercise should focus on the grammar/vocabulary concept of: {lesson_focus}."
        )
    prompt_parts.append(
        "Provide a sentence with a missing word, the options for the blank, and the correct answer. Format as a JSON object with 'sentence', 'options' (an array of strings), and 'answer' keys."
    )

    prompt = " ".join(prompt_parts)
    response = generate_llm_response(prompt)
    return {"exercise": clean_json_response(response)}


@router.post("/exercises/sentence-correction")
def correct_sentence(
    request: schemas.SentenceCorrectionRequest,
    current_user: models.User = Depends(get_current_user),
):
    """
    Corregge una frase scritta dall'utente e fornisce una spiegazione.
    """
    prompt = f"""A user is learning {request.target_language}. His native language is {current_user.native_language}.
    The user wrote the following sentence: '{request.sentence}'
    Please correct the sentence if there are any errors.
    Then, provide a brief, simple explanation of the correction in {current_user.native_language}.
    Format the output as a JSON object with 'corrected_sentence' and 'explanation' keys."""

    response = generate_llm_response(prompt)
    return {"correction": clean_json_response(response)}


@router.get("/exercises/comprehension-test")
def get_comprehension_test(
    target_language: str,
    current_user: models.User = Depends(get_current_user),
    topic: Optional[str] = None,
    lesson_focus: Optional[str] = None,
):
    """
    Genera un testo breve con domande a scelta multipla per testare la comprensione.
    """
    prompt_parts = [
        f"Generate a short text (about 3-4 paragraphs) in {target_language} for a language learner.",
        f"The user's native language is {current_user.native_language}.",
    ]
    if topic:
        prompt_parts.append(f"The topic should be about: {topic}.")
    else:
        prompt_parts.append("The topic should be about a daily life situation.")
    if lesson_focus:
        prompt_parts.append(
            f"The text should subtly incorporate examples of: {lesson_focus}."
        )
    prompt_parts.append(
        "After the text, create 3-4 multiple-choice questions about the text to test comprehension."
    )
    prompt_parts.append(f"The questions should be in {current_user.native_language}.")
    prompt_parts.append(
        "Format the entire output as a single JSON object with 'text' and 'questions' keys. The 'questions' should be an array of objects, each with 'question', 'options' (an array of strings), and 'answer' keys."
    )

    prompt = " ".join(prompt_parts)
    response = generate_llm_response(prompt)
    return {"comprehension_test": clean_json_response(response)}


@router.get("/exercises/flashcards")
def get_flashcards(
    target_language: str,
    current_user: models.User = Depends(get_current_user),
    topic: Optional[str] = None,
    lesson_focus: Optional[str] = None,
):
    """
    Genera 5 flashcard (parola e traduzione) relative a un argomento.
    """
    prompt_parts = [
        f"Generate 5 flashcards for learning {target_language}.",
        f"The user's native language is {current_user.native_language}.",
    ]
    if topic:
        prompt_parts.append(f"The flashcards should be related to the topic: {topic}.")
    if lesson_focus:
        prompt_parts.append(
            f"The flashcards should focus on vocabulary related to: {lesson_focus}."
        )
    prompt_parts.append(
        "For each flashcard, provide a word or short phrase in the target language and its translation in the user's native language. Format the output as a JSON array of objects, where each object has 'word_or_phrase' and 'translation' keys."
    )

    prompt = " ".join(prompt_parts)
    response = generate_llm_response(prompt)
    return {"flashcards": clean_json_response(response)}


@router.post("/exercises/submit-flashcard-correction")
def submit_flashcard_correction(
    request: schemas.FlashcardCorrectionRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Invia la traduzione di una flashcard per la correzione e aggiorna i progressi dell'utente.
    """
    user_progress = crud.get_or_create_progress(
        db, user_id=current_user.id, target_language=request.target_language
    )

    prompt = f"""A user learning {request.target_language} has provided a translation for a flashcard.
    Original text: '{request.flashcard_text}'
    User's translation: '{request.user_translation}'
    The user's native language is {current_user.native_language}.

    Please evaluate the user's translation. Provide two things in your response:
    1. A general feedback message for the user in {current_user.native_language}, explaining if the translation is correct or what could be improved.
    2. A JSON object with your evaluation of the vocabulary performance change. This JSON object must have one key: 'vocabulary_delta'. The value should be an integer: 1 for improvement, 0 for no change, or -1 for a step back.

    Format the entire output as a single JSON object with two keys: 'feedback' (a string) and 'evaluation' (the JSON object with the delta)."""

    response = generate_llm_response(prompt)

    try:
        response_data = clean_json_response(response)
        feedback = response_data.get("feedback", "Could not parse feedback.")
        evaluation = response_data.get("evaluation", {})

        crud.update_progress(
            db,
            progress_id=user_progress.id,
            vocabulary_delta=evaluation.get("vocabulary_delta", 0),
        )

    except (json.JSONDecodeError, AttributeError) as e:
        print(f"Error parsing LLM response: {e}")
        return {
            "feedback": "There was an error processing your results, but your submission has been received.",
            "new_progress": user_progress,
        }

    updated_progress = crud.get_or_create_progress(
        db, user_id=current_user.id, target_language=request.target_language
    )

    return {"feedback": feedback, "new_progress": updated_progress}
