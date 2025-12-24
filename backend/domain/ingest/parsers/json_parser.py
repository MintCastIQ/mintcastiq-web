import json
from pathlib import Path


class JSONChecklistParser:
    def __init__(self, file_path):
        self.file_path = Path(file_path)

    def parse(self):
        with self.file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        for row in data:
            yield row
