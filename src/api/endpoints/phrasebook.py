from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import schemas, crud, models
from database import SessionLocal
from utils.llm_handler import generate_llm_response, clean_json_response
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
import os
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


@router.get("/phrasebook")
def phrasebook(
    target_language: str,
    current_user: models.User = Depends(get_current_user),
    topic: Optional[str] = None,
):
    """
    Restituisce un elenco di frasi con traduzione per apprendere meglio la lingua.
    """
    prompt_parts = [
        f"Create a set of at least 30 useful sentences for a user who is learning the following language: {target_language}.",
        f"The user's native language is {current_user.native_language}.",
        f"Every sentence must have its own translation into the language {current_user.native_language}.",
        f"Answer just with the JSON content, without any other text.",
    ]
    if topic:
        prompt_parts.append(f"The topic should be about: {topic}.")

    prompt_parts.append(
        "Provide a JSON array of objects, where each object has 'sentence' and 'translation' keys"
    )

    prompt = " ".join(prompt_parts)
    response = generate_llm_response(prompt)
    return {"phrasebook": clean_json_response(response)}
