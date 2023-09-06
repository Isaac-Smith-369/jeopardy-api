from pydantic import BaseModel


class Question(BaseModel):
    id: str
    round: str
    category: str
    value: int = 100
    question: str
    answer: str
    seen: bool = False

class Game(BaseModel):
    questions: list[list[Question]]
    question_count: int