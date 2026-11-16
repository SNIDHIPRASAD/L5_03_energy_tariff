# Lab 5 – Reflection

**1. Which issues were the most important to fix, and why?**
The `eval()` call (Bandit B307) was the most important: it lets anyone who can type into the prompt run arbitrary Python on the machine. The mutable default argument and the bare `except:` were next, because they cause silent, hard-to-trace bugs rather than visible crashes.

**2. Which tool was most useful for which kind of problem?**
Bandit found the one real security hole and nothing else, so it is high signal. Pylint found the most issues (bugs, design smells, missing documentation) and its score gave a measurable goal (6.14 → 10.00). Flake8 was the quickest to fix, as it only enforces PEP 8 formatting, but it also caught the unused import and the bare `except`.

**3. What did the tools miss?**
No tool reported that a negative reading (`-50` units) was accepted and produced a negative electricity bill. That is a business-logic error that only appears when you run the program and read the output critically. Static analysis cannot know what the program is *supposed* to do, so it complements, but does not replace, testing and code review.

**4. How would you use static analysis in a real project?**
Run Flake8, Pylint and Bandit automatically in CI (or as pre-commit hooks) so every pull request is checked before merge, with Bandit findings and a minimum Pylint score blocking the build. Findings should be triaged by severity: security first, then bugs, then style. Occasional false positives can be silenced with a targeted, commented `# pylint: disable` / `# nosec` rather than by turning a check off globally.
