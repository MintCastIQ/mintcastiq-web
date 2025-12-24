from pathlib import Path

from domain.ingest.parsers.csv_parser import CSVChecklistParser
from domain.ingest.parsers.excel_parser import ExcelChecklistParser
from domain.ingest.parsers.json_parser import JSONChecklistParser


class ChecklistParserDispatcher:
    """
    Walks a directory and dispatches each file to the correct parser
    based on file extension. Yields raw rows with file-level provenance.
    """

    SUPPORTED_EXTENSIONS = {
        ".csv": CSVChecklistParser,
        ".xlsx": ExcelChecklistParser,
        ".json": JSONChecklistParser,
    }

    def __init__(self, directory_path):
        self.directory = Path(directory_path)

    def parse(self):
        if not self.directory.exists():
            raise FileNotFoundError(f"Directory not found: {self.directory}")

        for file_path in self.directory.iterdir():
            if not file_path.is_file():
                continue

            ext = file_path.suffix.lower()
            parser_cls = self.SUPPORTED_EXTENSIONS.get(ext)

            if not parser_cls:
                # Skip unsupported files silently or log it
                continue

            parser = parser_cls(file_path)

            for row in parser.parse():
                # Add provenance for audit clarity
                row["_file"] = file_path.name
                yield row
