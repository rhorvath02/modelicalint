import argparse
import sys
from pathlib import Path
from typing import List

from modelicalint.lint import lint_file


def collect_files(paths: List[str]) -> List[Path]:
    files: List[Path] = []
    for p in paths:
        path = Path(p)
        if path.is_dir():
            files.extend(sorted(path.rglob("*.mo")))
        else:
            files.append(path)
    return files


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="modelicalint",
        description="Style and structure linter for Modelica"
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="Modelica file(s) or directories"
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Automatically fix fixable issues"
    )

    args = parser.parse_args()

    files = collect_files(args.paths)
    if not files:
        print("No .mo files found")
        return 0

    had_error = False

    for file in files:
        messages, file_has_error = lint_file(
            file,
            apply_fixes=args.fix
        )

        for msg in messages:
            print(msg.format())

        if file_has_error:
            had_error = True

    return 1 if had_error else 0


if __name__ == "__main__":
    sys.exit(main())
