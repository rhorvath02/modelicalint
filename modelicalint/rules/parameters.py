from pathlib import Path
from typing import List

from modelicalint.rules.base import Rule
from modelicalint.message import LintMessage
from modelicalint.context import Context


class ParameterAnnotationRule(Rule):
    def __init__(self):
        super().__init__(
            code="ML401",
            description="Parameter missing Dialog annotation"
        )

    def check(self, path: Path, lineno: int, line: str, ctx: Context) -> List[LintMessage]:
        if line.strip().startswith("parameter") and "Dialog(" not in line:
            return [
                LintMessage(
                    str(path), lineno, 1,
                    self.code, self.description
                )
            ]
        return []
