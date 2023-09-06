from pathlib import Path
import logging
from app.models import Game
from app.queries import get_jeopardy_round
from fastapi import FastAPI

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.level = logging.DEBUG

CREATE_JEOPARDY_TABLE = """
    CREATE TABLE jeopardy (
        id INTEGER PRIMARY KEY,
        show_number TEXT,
        air_date DATE,
        round TEXT,
        category TEXT,
        value INTEGER,
        question TEXT,
        answer TEXT
    );
"""

INSERT_INTO_JEOPARDY = """
    INSERT INTO jeopardy (
        show_number,
        air_date,
        round,
        category,
        value,
        question,
        answer
    )
    VALUES (?, ?, ?, ?, ?, ?, ?);
"""

GET_JEOPARDY_CATEGORIES = """
    SELECT category FROM jeopardy
    ORDER BY RANDOM();
"""

GET_JEOPARARDY_QUESTIONS = """
    SELECT
        id,
        round,
        category,
        value,
        question,
        answer
    FROM jeopardy
    WHERE category = ?
    ORDER BY value;
"""

CWD = Path(__file__).parent.parent
CSV_PATH = CWD / "data/jeopardy.csv"
DB_PATH = CWD / "data/jeopardy.db"


def game():
    result = get_jeopardy_round(GET_JEOPARDY_CATEGORIES, GET_JEOPARARDY_QUESTIONS, DB_PATH)
    if result is None:
        logging.warning("No questions available")
        return
    game = Game.model_validate(result)
    return game


app = FastAPI()


@app.get("/")
def index():
    return "Welcome to jeopardy"

@app.get("/game")
def get_game():
    return game()