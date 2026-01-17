from pathlib import Path
from typing import List

from modelicalint.rules.base import Rule
from modelicalint.message import LintMessage
from modelicalint.context import Context
import re


class InlineAnnotationRule(Rule):
    def __init__(self):
        super().__init__(
            code="ML201",
            description="Inline annotation detected — move annotation to new line"
        )
        self.fixable = True

    def check(self, path: Path, lineno: int, line: str, ctx: Context) -> List[LintMessage]:
        stripped = line.strip()

        # Only apply to parameter declarations
        if not stripped.startswith("parameter "):
            return []

        # Ignore if annotation already moved
        if stripped.startswith("annotation("):
            return []

        if "annotation(" in line:
            before = line.split("annotation(", 1)[0]
            if before.strip():
                col = line.index("annotation(") + 1
                return [
                    LintMessage(
                        str(path),
                        lineno,
                        col,
                        self.code,
                        self.description
                    )
                ]

        return []

    def fix(self, line: str) -> List[str] | None:
        if "annotation(" not in line:
            return None

        indent = re.match(r"\s*", line).group(0)

        before, after = line.split("annotation(", 1)

        fixed = [
            before.rstrip() + "\n",
            indent + "annotation(" + after
        ]

        return fixed
