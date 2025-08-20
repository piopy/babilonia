from sqlalchemy.orm import Session
import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_username(db: Session, username: str):
    """
    Recupera un utente dal database tramite il suo nome utente.
    """
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    """
    Crea un nuovo utente nel database.
    """
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        username=user.username,
        hashed_password=hashed_password,
        native_language=user.native_language,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_or_create_progress(db: Session, user_id: int, target_language: str):
    """
    Crea o recupera il progresso di un utente per una specifica lingua target.
    """
    progress = (
        db.query(models.UserProgress)
        .filter_by(user_id=user_id, target_language=target_language)
        .first()
    )
    if not progress:
        progress = models.UserProgress(user_id=user_id, target_language=target_language)
        db.add(progress)
        db.commit()
        db.refresh(progress)
    return progress


def update_progress(
    db: Session,
    progress_id: int,
    comprehension_delta: int = 0,
    vocabulary_delta: int = 0,
    grammar_delta: int = 0,
):
    """
    Aggiorna il progresso di un utente per una specifica lingua target prendendo in considerazione i valori di comprensione del testo, vocabolario e grammatica.
    """
    progress = db.query(models.UserProgress).filter_by(id=progress_id).first()
    if progress:
        progress.comprehension_level += comprehension_delta
        progress.vocabulary_level += vocabulary_delta
        progress.grammar_level += grammar_delta
        progress.overall_progress = (
            progress.comprehension_level
            + progress.vocabulary_level
            + progress.grammar_level
        ) / 3.0
        db.commit()
        db.refresh(progress)
    return progress


def get_languages(db: Session):
    """
    Recupera tutte le lingue dal database.
    """
    return db.query(models.Language).order_by(models.Language.name).all()


def get_language_by_name(db: Session, name: str):
    """
    Recupera una lingua dal database tramite il nome.
    """
    return (
        db.query(models.Language)
        .filter(models.Language.name == name.capitalize())
        .first()
    )


def create_language(db: Session, name: str):
    """
    Aggiunge una nuova lingua al database.
    """
    db_language = models.Language(name=name)
    db.add(db_language)
    db.commit()
    db.refresh(db_language)
    return db_language


def get_topics(db: Session):
    """
    Recupera tutti i topics dal database.
    """
    return db.query(models.Topic).all()


def create_topic(db: Session, name: str):
    """
    Aggiunge un nuovo topic al database.
    """
    db_topic = models.Topic(name=name)
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic


def get_lesson_subjects(db: Session):
    """
    Recupera tutte gli argomenti di lezione dal database.
    """
    return db.query(models.LessonSubject).all()


def create_lesson_subject(db: Session, name: str):
    """
    Aggiunge un nuovo argomento di lezione al database.
    """
    db_lesson_subject = models.LessonSubject(name=name)
    db.add(db_lesson_subject)
    db.commit()
    db.refresh(db_lesson_subject)
    return db_lesson_subject
