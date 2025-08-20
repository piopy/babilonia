from fastapi import APIRouter, Depends, HTTPException, status
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


@router.get("/topics", response_model=List[schemas.Topic], tags=["Learning Content"])
def get_topics(db: Session = Depends(get_db)):
    """Ritorna una lista di tutti gli argomenti di lezione supportati per l'apprendimento."""
    return crud.get_topics(db)


@router.post("/topics", response_model=schemas.Topic, tags=["Learning Content"])
def create_topic(topic: schemas.TopicBase, db: Session = Depends(get_db)):
    """Aggiunge un nuovo argomento di lezione alla lista degli argomenti di lezione supportati."""
    db_topic = db.query(models.Topic).filter(models.Topic.name == topic.name).first()
    if db_topic:
        raise HTTPException(status_code=400, detail="Topic already exists")
    return crud.create_topic(db=db, name=topic.name)


@router.get(
    "/lesson-subjects",
    response_model=List[schemas.LessonSubject],
    tags=["Learning Content"],
)
def get_lesson_subjects(db: Session = Depends(get_db)):
    """Ritorna una lista di tutti gli argomenti di lezione supportati per l'apprendimento."""
    return crud.get_lesson_subjects(db)


@router.post(
    "/lesson-subjects", response_model=schemas.LessonSubject, tags=["Learning Content"]
)
def create_lesson_subject(
    subject: schemas.LessonSubjectBase, db: Session = Depends(get_db)
):
    """Aggiunge un nuovo argomento di lezione alla lista degli argomenti di lezione supportati."""
    db_subject = (
        db.query(models.LessonSubject)
        .filter(models.LessonSubject.name == subject.name)
        .first()
    )
    if db_subject:
        raise HTTPException(status_code=400, detail="Lesson subject already exists")
    return crud.create_lesson_subject(db=db, name=subject.name)
