from pathlib import Path
import logging
from app.models import Game
from app.queries import get_jeopardy_round
from fastapi import FastAPI

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.level = logging.DEBUG


CWD = Path(__file__).parent.parent
DB_PATH = CWD / "data/jeopardy.db"


def game():
    result = get_jeopardy_round(DB_PATH)
    if result is None:
        logging.warning("Couldn't retrieve jeopardy round")
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