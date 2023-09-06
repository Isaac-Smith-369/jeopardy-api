from typing import Hashable, Any
from pathlib import Path
import pandas as pd

def parse_jeopardy_csv(source: Path) -> list[dict[Hashable, Any]]:
    df = pd.read_csv(source)

    data = df.to_dict(orient='records')

    return data