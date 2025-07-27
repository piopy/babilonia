from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///../data/BabilonIA.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def init_db():
    import models
    import crud

    models.Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Populate initial languages
        initial_languages = [
            "English",
            "Spanish",
            "French",
            "German",
            "Italian",
            "Portuguese",
            "Dutch",
            "Russian",
            "Mandarin Chinese",
            "Japanese",
            "Korean",
        ]
        for lang_name in initial_languages:
            if not db.query(models.Language).filter_by(name=lang_name).first():
                crud.create_language(db, lang_name)

        # Populate initial topics
        initial_topics = [
            "Saluti e Presentazioni",
            "Viaggi e Trasporti",
            "Al Ristorante e Cibo",
            "Shopping e Negozi",
            "Lavoro e Professioni",
            "Famiglia e Amici",
            "Tempo Libero e Hobby",
            "Salute e Benessere",
            "Meteo e Stagioni",
            "In Città e Indicazioni Stradali",
        ]
        for topic_name in initial_topics:
            if not db.query(models.Topic).filter_by(name=topic_name).first():
                crud.create_topic(db, topic_name)

        # Populate initial lesson subjects
        initial_lesson_subjects = [
            "Articoli (Determinativi e Indeterminativi)",
            "Sostantivi (Genere e Numero)",
            "Aggettivi (Accordo e Posizione)",
            "Pronomi (Personali, Possessivi, Dimostrativi)",
            "Verbi: Presente Indicativo",
            "Verbi: Passato Prossimo",
            "Verbi: Imperfetto",
            "Verbi: Futuro Semplice",
            "Preposizioni (Semplici e Articolate)",
            "Congiunzioni",
            "Avverbi",
        ]
        for subject_name in initial_lesson_subjects:
            if not db.query(models.LessonSubject).filter_by(name=subject_name).first():
                crud.create_lesson_subject(db, subject_name)

    finally:
        db.close()
