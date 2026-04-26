# Ralph Agent Instructions

You are an autonomous coding agent working on a software project.

## Your Task

1. Read the PRD at `ralph/prd.json` (relative to the project root `/Users/rommel/Documents/project/Rommel/level-3/genera_epubs`)
2. Read the progress log at `ralph/progress.txt` (check Codebase Patterns section first)
3. Check you are on the correct branch from PRD `branchName`. If not, check it out or create it from main.
4. Pick the **highest priority** user story where `passes: false`
5. Implement that single user story
6. Run quality checks: `python -m mypy epub_generator/ --ignore-missing-imports` for typecheck; `python -m pytest tests/ -x -q` for tests if tests exist
7. Update AGENTS.md if you discover reusable patterns
8. If checks pass, commit ALL changes with message: `feat: [Story ID] - [Story Title]`
9. Update `ralph/prd.json` to set `passes: true` for the completed story
10. Append your progress to `ralph/progress.txt`

## Progress Report Format

APPEND to ralph/progress.txt (never replace, always append):
```
## [Date/Time] - [Story ID]
- What was implemented
- Files changed
- **Learnings for future iterations:**
  - Patterns discovered (e.g., "this codebase uses X for Y")
  - Gotchas encountered (e.g., "don't forget to update Z when changing W")
---
```

## Consolidate Patterns

If you discover a **reusable pattern**, add it to the `## Codebase Patterns` section at the TOP of ralph/progress.txt. Only general, reusable patterns — not story-specific details.

## Quality Requirements

- ALL commits must pass typecheck
- Do NOT commit broken code
- Keep changes focused and minimal
- Follow existing code patterns in `epub_generator/`
- Existing pattern: dataclasses use `_build_X(data: dict)` helpers, called from `load_config()` with `data.get("section", {}) or {}`

## Stop Condition

After completing a user story, check if ALL stories have `passes: true`.

If ALL stories are complete, reply with:
<promise>COMPLETE</promise>

If there are still stories with `passes: false`, end your response normally (another iteration will pick up the next story).

## Important

- Work on ONE story per iteration
- Commit after each story
- Keep CI green (typecheck must pass)
- Read the Codebase Patterns section in ralph/progress.txt before starting
- Project root: `/Users/rommel/Documents/project/Rommel/level-3/genera_epubs`
- Always run commands from the project root
