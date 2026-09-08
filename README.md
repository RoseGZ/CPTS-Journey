# CPTS-Journey
Daily notes and reflections from my journey through HTB Academy's Penetration Tester path toward the CPTS (Certified Penetration Testing Specialist) certification.

## How this journal works

- Written day-to-day in Obsidian, one note per day in `journal/`, from the template in `templates/daily-template.md`.
- The [Obsidian Git](https://github.com/Vinzent03/obsidian-git) plugin auto-commits and pushes changes every ~20 minutes while the vault is open, and pulls on startup — no manual git commands needed day to day.
- A pre-commit hook (`.githooks/`) does a lightweight scan of staged notes for obvious secrets, internal IPs, or company identifiers before anything is committed, as a safety net. On a fresh clone, enable it once with:
  ```
  git config core.hooksPath .githooks
  ```

## Ground rules for what goes in here

This is a public journal, not a write-up repo:

- No HTB certification exam content — CPTS exam material is covered by HTB's NDA and never gets posted here, under any framing.
- No exact flags or full step-by-step walkthroughs of active Machines/Challenges (general topics, techniques, and reflections are fine; HTB's terms restrict solution-sharing for active content).
- No client, employer, or company-confidential information — no RAVEN client names, engagements, or internal details.
- No credentials, tokens, internal IPs/hostnames, or other technical secrets.
- No personal/private information beyond what I'm comfortable being public.
