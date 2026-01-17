from pathlib import Path
from typing import List

from modelicalint.rules.base import Rule
from modelicalint.message import LintMessage
from modelicalint.context import Context


class WithinRule(Rule):
    def __init__(self):
        super().__init__(
            code="ML010",
            description="'within' declaration must be the first statement",
            severity="error"
        )

    def check(self, path: Path, lineno: int, line: str, ctx: Context) -> List[LintMessage]:
        stripped = line.strip()

        if not hasattr(ctx, "seen_nonempty"):
            ctx.seen_nonempty = False

        if not stripped or stripped.startswith("//"):
            return []

        if stripped.startswith("within "):
            if ctx.seen_nonempty:
                return [
                    LintMessage(
                        str(path), lineno, 1,
                        self.code, self.description,
                        severity="error"
                    )
                ]
            ctx.seen_nonempty = True
            return []

        ctx.seen_nonempty = True
        return []


class SingleModelRule(Rule):
    def __init__(self):
        super().__init__(
            code="ML011",
            description="Multiple top-level definitions in file"
        )
        self.seen = 0

    def check(self, path: Path, lineno: int, line: str, ctx: Context) -> List[LintMessage]:
        if lineno == 1:
            self.seen = 0

        stripped = line.strip()

        if not stripped or stripped.startswith("//"):
            return []

        if stripped.startswith(("within ", "annotation(", "extends ")):
            return []

        if stripped.startswith((
            "model ",
            "partial model ",
            "package ",
            "record ",
            "block ",
            "function "
        )):
            self.seen += 1
            if self.seen > 1:
                return [
                    LintMessage(
                        str(path),
                        lineno,
                        1,
                        self.code,
                        self.description
                    )
                ]

        return []
