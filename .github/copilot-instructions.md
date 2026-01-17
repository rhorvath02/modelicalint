# AI Coding Guidelines for modelicalint

modelicalint is a pure Python linter for Modelica (.mo) files, processing line-by-line with stateful rules. This guide covers architecture, development workflows, and project conventions.

## Architecture Overview
modelicalint is a rule-based linter for Modelica (.mo) files that processes files line-by-line using a Context object to maintain state across lines. The core flow:
- `cli.py` collects .mo files and calls `lint.py::lint_file()` for each
- `lint_file()` iterates through lines, applying all enabled rules from `rules/`
- Rules can emit `LintMessage` objects and optionally provide fixes
- If `--fix` is used, fixed lines are written back and linting re-runs

## Key Components
- **Rules**: Extend `Rule` dataclass from `rules/base.py`, implement `check(path, lineno, line, ctx)` returning `LintMessage` list
- **Context**: Tracks state like current section, top-level definitions, seen_within (see `context.py`)
- **Messages**: Use `LintMessage(path, line, col, code, message, severity)` with codes like "ML201"
- **Configuration**: `modelicalint.toml` enables/disables rules and specifies legacy ignore patterns

Example config:
```toml
[rules]
ML201 = true   # no inline annotations
ML301 = true   # parameters require Dialog

[legacy]
ignore = [
  "VehicleDynamics/Utilities/**",
  "VehicleDynamics/TestUtilities/**"
]
```

## Adding a New Rule
1. Create a new class in `rules/` extending `Rule` from `rules/base.py`
2. Implement `check(self, path, lineno, line, ctx)` to return list of `LintMessage`s
3. For fixable rules: set `fixable=True` and implement `fix(self, line)` returning list of replacement lines or None
4. Import the class in `rules/__init__.py` and add to `ALL_RULES`
5. Update `modelicalint.toml` to enable/disable the rule (use MLxxx codes)
6. Test manually: `modelicalint path/to/file.mo` or `modelicalint .`

## Examples from Codebase
- **InlineAnnotationRule** (`rules/annotations.py`): Detects inline annotations on parameters, moves them to new lines with proper indentation
- **SectionOrderRule** (`rules/sections.py`): Enforces section ordering using context to track current section
- **ConnectPlacementRule** (`rules/connects.py`): Ensures connect() calls are inside equation sections

## Development Patterns
- **Context Usage**: Rules modify ctx attributes to track state (e.g., `ctx.section = "equation"`)
- **Output Format**: Messages format as "path:line:col: MLxxx message" (matches VS Code problem matcher in `.vscode/tasks.json`)
- **Testing**: No formal test suite; manually test with `modelicalint .` or specific files

## VS Code Integration
- Run linting via "Modelica Lint" task (Ctrl+Shift+P → Tasks: Run Task)
- Problem matcher parses output for editor integration
- Use `--fix` flag for automatic corrections

## Code Style Notes
- Pure Python (no external dependencies)
- Rules use regex for pattern matching on stripped lines
- Fixes preserve indentation using `re.match(r"\s*", line).group(0)`
- Context prevents duplicate checks (e.g., ignore annotation lines after moving)

## Best Practices
- Always test rules on real .mo files before committing
- Use context for state that spans multiple lines (e.g., section tracking)
- Fixable rules should handle indentation correctly to avoid breaking code structure
- Message codes follow MLxxx pattern; increment for new rules
- Re-run linting after fixes to catch any new issues introduced