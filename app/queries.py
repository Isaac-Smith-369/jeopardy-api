import logging
from app.db import DevDB
from pathlib import Path
from typing import Any
from app.models import Question

def get_jeopardy_data(query: str, source: Path, limit: int = 2) -> list[tuple[Any]] | None:
    logging.info("Retrieving jeopardy data")
    with DevDB(str(source)) as (_, cursor):
        try:
            cursor.execute(query)
            result = cursor.fetchmany(limit)
            return result
        except Exception:
            logging.exception("Failed to retrieve jeopardy data")


def get_jeopardy_questions(query: str, source: Path, category: tuple[str], limit: int = 2) -> list[Question] | None:
    logging.info("Retrieving jeopardy questions")
    with DevDB(str(source)) as (_, cursor):
        try:
            cursor.execute(query, category)
            result = cursor.fetchmany(limit)
            questions = [Question(id=str(q[0]), round=q[1],category=q[2],value=q[3],question=q[4],answer=q[5],) for q in result]
            return questions
        except Exception:
            logging.exception("Failed to retrieve jeopardy questions")

def get_jeopardy_round(source: Path) -> dict[str, list[list[Question]] | int] | None:
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

    logging.info("Retrieving jeopardy round")
    # get 5 random categories and then use those categories to fetch the rounds
    categories = get_jeopardy_data(GET_JEOPARDY_CATEGORIES, source, 3)

    if categories is None:
        logging.warning("No categories available")
        return

    questions: list[list[Question]] = []
    count: int = 0

    for category in categories:

        questions_set = get_jeopardy_questions(GET_JEOPARARDY_QUESTIONS, source, category, 5)

        if questions_set is None:
            logging.warning("No questions available for these categories")
            return

        questions.append(questions_set)
        count += len(questions_set)

    return dict(questions=questions, question_count=count)