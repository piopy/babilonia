from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
import crud, schemas, models
from database import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/languages", response_model=List[schemas.Language])
def get_languages(db: Session = Depends(get_db)):
    """
    Ritorna una lista di tutte le lingue supportate per l'apprendimento.
    """
    return crud.get_languages(db)


@router.post("/add-language", response_model=schemas.Language)
def add_language(language: schemas.LanguageBase, db: Session = Depends(get_db)):
    """
    Aggiunge una nuova lingua alla lista delle lingue supportate.
    """
    db_language = (
        db.query(models.Language).filter(models.Language.name == language.name.capitalize()).first()
    )
    if db_language:
        raise HTTPException(status_code=400, detail="Language already in list")
    return crud.create_language(db=db, name=language.name.capitalize())
