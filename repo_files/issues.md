# Lab 5 – Issue Table (`energy_system.py`)

Baseline: **Pylint 6.14/10**, **Bandit 1 Medium**, **Flake8 12 warnings**.
Final: **Pylint 10.00/10**, **Bandit 0 issues**, **Flake8 0 warnings**.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| `eval()` on user input (Bandit B307 / Pylint W0123) | Security (Medium) | 63 | `eval(adjustment)` executes whatever the user types, e.g. `__import__('os').system(...)` = arbitrary code execution. | Replaced with `safe_eval()`, which parses with `ast` and only allows numbers and `+ - * /`. Anything else raises `ValueError`, which `main()` catches. |
| Mutable default argument `history=[]` (Pylint W0102) | Bug | 12 | The same list is shared by every call, so history leaks across calls and callers. | Default is now `None`; a new list is created inside the function. `main()` owns its own `history` list. |
| Negative meter reading accepted (**not flagged by any tool**) | Logic bug | 14, 55, 60 | `record_reading("M-03", -50)` was stored and produced a **negative bill (-192.50)**. | `record_reading()` validates that units are a finite, non-negative number and raises `ValueError`; `main()` reports the rejection and `compute_bill` for an unknown meter is handled via `KeyError`. |
| Bare `except:` (Pylint W0702 / Flake8 E722) | Bug / Style | 44 | Swallows every error, including `KeyboardInterrupt`, hiding real failures. | Catches only `(OSError, json.JSONDecodeError)`; also checks the loaded JSON is a dict. |
| Files opened without `with` / encoding (Pylint R1732, W1514) | Resource leak | 42, 48 | File handles could leak if an exception occurs; encoding depended on the OS. | `with open(file, encoding="utf-8") as handle:` and `json.load` / `json.dump`. |
| `global` statements (Pylint W0603) | Design | 27, 40 | Rebinding module globals makes state hard to follow and test; `raise_rates` permanently mutated constants. | State kept in module-level containers (`METERS`, `RATES`) that are modified in place; no `global` needed. |
| Unused import `sys` (Pylint W0611 / Flake8 F401) | Style | 2 | Dead import. | Removed. |
| Missing docstrings (Pylint C0114, C0116 ×7) | Documentation | 1, 12-52 | Module and every function lacked a docstring. | Added concise docstrings. |
| `elif` after `return` (Pylint R1705) | Style | 19-24 | Unnecessary `elif/else` chain after `return`. | Flattened to sequential `if` statements; magic numbers 100/300 became `TIER_1_LIMIT` / `TIER_2_LIMIT`. |
| `%`-formatting (Pylint C0209) | Style | 59, 60, 66 | Old-style string formatting. | Converted to f-strings. |
| `main()` runs on import | Design | 68 | Importing the module executes the program (breaks testing/reuse). | Added `if __name__ == "__main__":` guard. |
| Blank lines / long lines (Flake8 E302 ×7, E305, E501 ×2) | Formatting | 12-68 | Two blank lines required between top-level definitions; lines over 79 chars. | Reformatted to PEP 8 (2 blank lines, wrapped long expressions). |
