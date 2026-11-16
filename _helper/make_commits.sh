#!/usr/bin/env bash
# Usage: bash make_commits.sh /path/to/cloned/L5_03_energy_tariff
# Creates the 3 required commits (Bandit -> Pylint -> Flake8) in your clone.
set -e
REPO="$1"; HERE="$(cd "$(dirname "$0")" && pwd)"; FILES="$HERE/../repo_files"
[ -d "$REPO/.git" ] || { echo "Give the path of your cloned repo"; exit 1; }
cd "$REPO"
mkdir -p reports/before reports/after
cp "$FILES"/reports/before/* reports/before/

cp "$HERE/stages/energy_system_stage1_bandit.py" energy_system.py
git add energy_system.py reports/before
git commit -m "Fix Bandit issue: replace eval() with safe AST-based arithmetic evaluator"

cp "$HERE/stages/energy_system_stage2_pylint.py" energy_system.py
git add energy_system.py
git commit -m "Fix Pylint issues: mutable default, bare except, globals, docstrings, with-open, validation (score 10/10)"

cp "$HERE/stages/energy_system_stage3_flake8.py" energy_system.py
cp "$FILES"/reports/after/* reports/after/
cp "$FILES"/issues.md "$FILES"/reflection.md .
git add energy_system.py reports/after issues.md reflection.md
git commit -m "Fix Flake8 formatting issues; add after-reports, issues table and reflection"
echo "Done. Now run: git push"
