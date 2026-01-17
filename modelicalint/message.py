from pathlib import Path


class LintMessage:
    def __init__(self, path: str, line: int, col: int, code: str, message: str, severity: str = "warning"):
        self.path = path
        self.line = line
        self.col = col
        self.code = code
        self.message = message
        self.severity = severity

    def format(self) -> str:
        return f"{self.path}:{self.line}:{self.col}: {self.code} {self.message}"

    def __str__(self) -> str:
        return self.format()
