from pathlib import Path
from typing import List, Tuple

from modelicalint.rules import ALL_RULES
from modelicalint.context import Context
from modelicalint.message import LintMessage


def lint_file(path: Path, apply_fixes: bool = False) -> Tuple[List[LintMessage], bool]:
    ctx = Context()
    messages: List[LintMessage] = []
    new_lines: List[str] = []

    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for lineno, line in enumerate(lines, start=1):
        fixed_line = None

        for rule in ALL_RULES:
            msgs = rule.check(path, lineno, line, ctx)
            if msgs:
                messages.extend(msgs)

                if apply_fixes and getattr(rule, "fixable", False):
                    fixed = rule.fix(line)
                    if fixed is not None:
                        fixed_line = fixed
                        break

        if fixed_line is not None:
            # rule.fix returns a list[str]
            new_lines.extend(fixed_line)
        else:
            new_lines.append(line)

    # ✨ WRITE FIXES
    if apply_fixes and new_lines != lines:
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

        # 🔁 IMPORTANT: re-run lint on the updated file
        return lint_file(path, apply_fixes=False)

    has_error = any(m.severity == "error" for m in messages)
    return messages, has_error
