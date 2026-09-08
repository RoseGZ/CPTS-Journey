# CPTS-Journey
Daily notes and reflections from my journey through HTB Academy's Penetration Tester path toward the CPTS (Certified Penetration Testing Specialist) certification.

## How this journal works

- Written day-to-day in Obsidian, one note per day in `journal/`, from the template in `templates/daily-template.md`.
- A pre-commit hook (`.githooks/`) does a lightweight scan of staged notes for obvious secrets, internal IPs, or identifiers before anything is committed, as a safety net. On a fresh clone, enable it once with:
  ```
  git config core.hooksPath .githooks
  ```


