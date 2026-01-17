from pathlib import Path
from typing import List

from modelicalint.rules.base import Rule
from modelicalint.message import LintMessage
from modelicalint.context import Context


class ConnectPlacementRule(Rule):
    def __init__(self):
        super().__init__(
            code="ML501",
            description="connect() should be grouped in equation section"
        )

    def check(self, path: Path, lineno: int, line: str, ctx: Context) -> List[LintMessage]:
        if "connect(" in line and ctx.section != "equation":
            return [
                LintMessage(
                    str(path), lineno, 1,
                    self.code, self.description
                )
            ]
        return []
