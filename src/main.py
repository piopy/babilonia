from fastapi import FastAPI
from api.endpoints import auth, languages, exercises, learning_content, phrasebook, chat
from database import engine, Base, init_db

Base.metadata.create_all(bind=engine)
init_db() 

app = FastAPI(
    title="Babilonia API",
    description="API per un'applicazione di apprendimento linguistico tramite LLM.",
    version="0.1.0",
)

app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(languages.router, prefix="/api", tags=["Languages"])
app.include_router(exercises.router, prefix="/api", tags=["Exercises"])
app.include_router(learning_content.router, prefix="/api", tags=["Learning Content"])
app.include_router(phrasebook.router, prefix="/api", tags=["Phrasebook"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])


@app.get("/")
def read_root():
    return {"message": "Welcome to Babilonia!"}
