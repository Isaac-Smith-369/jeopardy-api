import logging
from app.db import DB
from pathlib import Path
from typing import Any, Hashable
from app.models import Question
from app.utils import parse_jeopardy_csv


def create_table(query: str, source: Path):
    logging.info("Creating database table")
    with DB(str(source)) as (_, cursor):
        try:
            cursor.execute(query)
            logging.info("Finished creating table")
        except Exception:
            logging.exception("Failed to create database")

def insert_into_table(query: str, source: Path, data: list[tuple[Any]]):
    logging.info("Inserting data into database")
    with DB(str(source)) as (connection, cursor):
        try:
            for record in data:
                cursor.execute(query, record)
                connection.commit()
            logging.info("Finished inserting data")
        except Exception:
            logging.exception("Failed to insert into database")

def seed_jeopardy_db(query: str, db_path: Path, csv_path: Path):
    logging.info("Seeding jeopardy database")
    records = []

    data = parse_jeopardy_csv(csv_path)

    for i, d in enumerate(data):

        if i == 1005:
            break

        # print(d["Value"])
        value: int = int(d["Value"].replace("$", "").replace(",", "")) if isinstance(d["Value"], str) else 200
        tmp = (
            d["Show Number"],
            d["Air Date"],
            d["Round"],
            d["Category"],
            value,
            d["Question"],
            d["Answer"]
        )
        records.append(tmp)

    insert_into_table(query, db_path, records)
    logging.info("Finished seeding jeopardy database")


def get_jeopardy_data(query: str, source: Path, limit: int = 2) -> list[tuple[Any]] | None:
    logging.info("Retrieving jeopardy data")
    with DB(str(source)) as (_, cursor):
        try:
            cursor.execute(query)
            result = cursor.fetchmany(limit)
            return result
        except Exception:
            logging.exception("Failed to retrieve jeopardy data")

def get_jeopardy_questions(query: str, source: Path, category: tuple[str], limit: int = 2) -> list[Question] | None:
    logging.info("Retrieving jeopardy questions")
    with DB(str(source)) as (_, cursor):
        try:
            cursor.execute(query, category)
            result = cursor.fetchmany(limit)
            questions = [Question(id=str(q[0]), round=q[1],category=q[2],value=q[3],question=q[4],answer=q[5],) for q in result]
            return questions
        except Exception:
            logging.exception("Failed to retrieve jeopardy questions")


def get_jeopardy_round(categories_query: str, questions_query: str, source: Path) -> dict[str, list[list[Question]] | int] | None:
    logging.info("Retrieving jeopardy round")
    # get 5 random categories and then use those categories to fetch the rounds
    categories = get_jeopardy_data(categories_query, source, 3)

    if categories is None:
        logging.warning("No categories available")
        return

    questions: list[list[Question]] = []
    count: int = 0

    for category in categories:

        questions_set = get_jeopardy_questions(questions_query, source, category, 5)

        if questions_set is None:
            logging.warning("No questions available for these categories")
            return

        questions.append(questions_set)
        count += len(questions_set)

    return dict(questions=questions, question_count=count)

