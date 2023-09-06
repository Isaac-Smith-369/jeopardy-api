from app.queries import seed_jeopardy_db, create_table
from pathlib import Path
import logging


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.level = logging.DEBUG


CWD = Path(__file__).parent
CSV_PATH = CWD / "data/jeopardy.csv"
DB_PATH = CWD / "jeopardy.db"


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



def main():
    create_table(CREATE_JEOPARDY_TABLE, DB_PATH)
    seed_jeopardy_db(INSERT_INTO_JEOPARDY, DB_PATH, CSV_PATH)



if __name__ ==  "__main__":
    main()