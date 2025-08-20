from pydantic import BaseModel
from typing import List, Optional

# Qui ci sono tutte le classi utilizzate in Fastapi/Pydantic per la validazione dei dati

class UserBase(BaseModel):
    username: str
    native_language: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserProgress(BaseModel):
    target_language: str
    comprehension_level: int = 1
    vocabulary_level: int = 1
    grammar_level: int = 1
    overall_progress: float = 0.0

    class Config:
        orm_mode = True


class AssessmentAnswer(BaseModel):
    question: str
    user_answer: str


class AssessmentSubmission(BaseModel):
    exercise_type: str  # ad esempio "comprehension-test", "fill-in-the-blank", ...
    target_language: str
    answers: List[AssessmentAnswer]


class FlashcardCorrectionRequest(BaseModel):
    flashcard_text: str
    user_translation: str
    target_language: str


class LanguageBase(BaseModel):
    name: str


class Language(LanguageBase):
    id: int

    class Config:
        orm_mode = True


class TopicBase(BaseModel):
    name: str


class Topic(TopicBase):
    id: int

    class Config:
        orm_mode = True


class LessonSubjectBase(BaseModel):
    name: str


class LessonSubject(LessonSubjectBase):
    id: int

    class Config:
        orm_mode = True

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatInteractionRequest(BaseModel):
    language: str
    mode: str
    messages: List[ChatMessage]

class SentenceCorrectionRequest(BaseModel):
    sentence: str
    target_language: str
