# modelicalint

A style and structure linter for Modelica (.mo) files. Ensures consistent code formatting, proper component organization, and adherence to Modelica best practices.

## Features

- **Line-by-line processing** with stateful rules for complex validations
- **Auto-fixing** for common style issues
- **VS Code integration** with problem matchers
- **Configurable rules** via TOML configuration
- **Pure Python** with no external dependencies

## Installation

```bash
pip install .
```

Or for development:
```bash
pip install -e .
```

## Usage

```bash
# Lint a single file
modelicalint path/to/file.mo

# Lint all .mo files in directory (recursive)
modelicalint .

# Auto-fix fixable issues
modelicalint --fix .

# Check exit code (0 = success, 1 = errors found)
echo $?  # Use in CI/CD pipelines
```

## Rules

modelicalint enforces the following rules:

### ML201: No Inline Annotations
**Severity:** Warning  
**Fixable:** Yes  
**Description:** Parameter annotations must be on separate lines for readability.

**Bad:**
```modelica
parameter Real x = 1 annotation(Dialog(tab="General"));
```

**Good:**
```modelica
parameter Real x = 1
  annotation(Dialog(tab="General"));
```

### ML301: Section Ordering
**Severity:** Warning  
**Fixable:** No  
**Description:** Ensures proper ordering of Modelica class sections.

**Required order:** `import` → `parameter` → `protected` → `public` → `equation` → `algorithm`

### ML401: Parameters Require Dialog
**Severity:** Warning  
**Fixable:** No  
**Description:** All parameters should have Dialog annotations for proper UI integration.

**Bad:**
```modelica
parameter Real x = 1;
```

**Good:**
```modelica
parameter Real x = 1 annotation(Dialog(tab="General"));
```

### ML501: Connect in Equation Section
**Severity:** Warning  
**Fixable:** No  
**Description:** `connect()` statements must be placed inside equation sections.

**Bad:**
```modelica
model BadExample
  // ... components ...
  connect(a, b);  // Wrong: outside equation section
end BadExample;
```

**Good:**
```modelica
model GoodExample
  // ... components ...
equation
  connect(a, b);  // Correct: inside equation section
end GoodExample;
```

### ML010: Within Declaration First
**Severity:** Error  
**Fixable:** No  
**Description:** `within` declarations must be the first non-comment statement in a file.

### ML011: Single Top-Level Definition
**Severity:** Warning  
**Fixable:** No  
**Description:** Files should contain only one top-level model/package/class definition.

## Configuration

Create or edit `modelicalint.toml` in your project root:

```toml
[rules]
ML201 = true   # no inline annotations
ML301 = true   # section ordering
ML401 = true   # parameters require Dialog
ML501 = true   # connect() inside equation

[legacy]
ignore = [
  "OldLibrary/**",  # Skip legacy code
  "VendorCode/**"
]
```

## VS Code Integration

1. **Tasks Configuration**: The `.vscode/tasks.json` provides the "Modelica Lint" task
2. **Run Linting**: `Ctrl+Shift+P` → "Tasks: Run Task" → "Modelica Lint"
3. **Problem Panel**: Errors and warnings appear in VS Code's Problems panel with clickable links

## Development

### Adding New Rules

1. Create a new rule class in `modelicalint/rules/` extending `Rule`
2. Implement `check()` method returning `List[LintMessage]`
3. For fixable rules, implement `fix()` returning `List[str]` or `None`
4. Add to `ALL_RULES` in `rules/__init__.py`
5. Update `modelicalint.toml` with the new rule code

### Testing

```bash
# Test on sample files
modelicalint test_files/

# Verify fixes work
modelicalint --fix test_files/ && modelicalint test_files/
```

## Exit Codes

- `0`: No issues found
- `1`: Issues found (warnings/errors)

## License

MIT License