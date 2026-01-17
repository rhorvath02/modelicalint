from pathlib import Path
from typing import List

from modelicalint.rules.base import Rule
from modelicalint.message import LintMessage
from modelicalint.context import Context


SECTION_ORDER = [
    "import",
    "parameter",
    "protected",
    "public",
    "equation",
    "algorithm"
]


class SectionOrderRule(Rule):
    def __init__(self):
        super().__init__(
            code="ML301",
            description="Section order violation"
        )

    def check(self, path: Path, lineno: int, line: str, ctx: Context) -> List[LintMessage]:
        stripped = line.strip()
        for section in SECTION_ORDER:
            if stripped.startswith(section):
                if ctx.section and SECTION_ORDER.index(section) < SECTION_ORDER.index(ctx.section):
                    return [
                        LintMessage(
                            str(path), lineno, 1,
                            self.code, self.description
                        )
                    ]
                ctx.section = section
        return []
