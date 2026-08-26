# AGENTS.md

Guide for agents working on SmartRecommender. Add a section per area as
conventions emerge — do not pad sections with content that is not established
yet.

## What this project is

A fullstack product recommendation platform: Django REST on the backend, React
18 on the frontend, PostgreSQL for persistence, containerised with Docker. It
implements **six recommendation methods written from scratch** rather than
pulled from a recommender library — collaborative filtering, content-based
filtering, association rules, fuzzy search, probabilistic methods and sentiment
analysis.

Read [README.md](README.md) for the architecture, the Docker workflow and the
API surface. The detailed project context lives in
[.claude/skills.md](.claude/skills.md) — read it before changing recommendation
code so you do not re-derive what is already documented.

## Language

**UI copy and code comments are English.** Labels, buttons, validation messages,
page titles, empty states and error text are all English. User-supplied data
(product names, review text) is rendered exactly as entered and never
normalised.

## Comments

Comments explain **why**, not what. The code already says what it does.

- Use multi-line block comments for anything that needs explaining; avoid
  trailing one-line comments tacked onto the end of a statement.
- A comment that restates the code is deleted rather than reworded.
- For a recommendation method, document the assumption it rests on and the
  failure mode it guards against — that is what a reader cannot recover from
  the implementation alone.

## Recommendation methods

Each method is self-contained and ships with its own UML documentation under
`.diagrams/<method>/` and debug views in the admin panel. When you change a
method:

- Keep the diagrams in step with the code, or delete the ones that no longer
  describe reality — a stale diagram is worse than none.
- The methods are deliberately dependency-free. Do not replace one with a
  library call; the point of the project is the implementation.

## Database

Schema changes go through Django migrations — never edit a committed migration.
The ERD under `.database/entity-relationship-diagram/` documents the schema and
should be regenerated when the models change.

## Before finishing

- [ ] The stack boots: `docker compose -f .tools/docker/docker-compose.yml up --build`.
- [ ] Migrations apply cleanly against an empty database.
- [ ] No secrets, tokens or personal data committed.
- [ ] README updated when behaviour, commands or structure changed.
- [ ] Copy is English.
