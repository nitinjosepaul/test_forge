# Copilot Instructions — test_forge

Personal learning / interview-prep project: a **deterministic Flaky Test Detector**
(Python + pytest) that analyzes the last N JUnit XML reports and classifies each
test as Stable / Suspect / Flaky, gated in CI.

## Resuming work (read first)
1. `resource/tracking/status/STATUS.txt` — current snapshot
2. `resource/tracking/testforgeworks/current.txt` — current Kanban board (in-flight work)
3. `README.txt` — stable design and architecture

## Working agreement
- **Plan before big changes.** For restructures or multi-file changes: analyze,
  propose the approach, wait for approval, then execute in one shot.
- **Ask when in doubt** (e.g. which files to move/delete) before changing anything.
- **Keep responses concise.** Status updates cover only the current update — no recap.
- **The user decides when to commit.** When asked, draft a brief, bulleted commit
  message ending with the trailer:
  `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`
- **Before a commit, refresh git state** — check for untracked/missing files and
  add them.
- Use `git mv` / `git rm` for tracked files so history is preserved.
- Environment: Windows + PowerShell, Windows-style paths.

## Documentation rules
- **README.txt = stable design/architecture only.** No status, sprint progress,
  or current-demo details.
- **Review README.txt whenever a design decision changes** and update it if
  necessary. If the change is a **major design change**, tell the user
  explicitly and get approval before editing README.
- **Tracking lives under `resource/tracking/`:**
  - `status/STATUS.txt` — live snapshot, overwritten in place, with a
    "Last updated" date.
  - `status/CHANGELOG.txt` — append-only history, newest at top, never rewrite
    the content of past entries. **Exactly one entry per day**: multiple
    same-day changes are bullets under a single `[YYYY-MM-DD]` heading.
  - `demo/[YYYY.MM.DD] DemoN/` — one folder per demo (`presentation_deck.txt`,
    `action_items.txt`). Binary decks/exports (`*.pdf`, `*.pptx`) are kept
    local only and gitignored — pushing them is blocked on this network.
  - `testforgeworks/current.txt` + `backlog.txt` — Kanban board.
  - `testforgeworks/archive/` — superseded per-sprint files, reference only.
- Docs use the repo's existing `.txt` format. Don't create new markdown files for
  planning/notes.

## Kanban / sprint conventions
- Hierarchy: **Feature → Story → Task**. Tasks are sized **1–2 days**; split
  anything bigger.
- Open Tasks use JIRA-import-ready format:
  ```
  Summary: <one liner>
  Description: <details>
  Original Estimate: <1d|2d|TBD>
  ```
  Completed work is listed as plain historical notes (not tickets).
- Only the current sprint is planned in detail. Everything else stays in the
  unscheduled backlog and is pulled onto `current.txt` deliberately.
- Demo action items go into the **current sprint**, not the backlog.

## Design guardrails
- pytest is the sole execution engine.
- `framework/` (the detector) never imports from plugins or pytest internals —
  it only reads JUnit XML from disk. Pipeline:
  `normalize -> classify -> impact -> reporting -> cli`.
- Classification, confidence, and the CI gate are **deterministic** and the
  source of truth. AI summarization is optional, additive, and never influences
  labels or gate decisions.
- `run_id` / `timestamp_utc` come from the XML `<testsuite timestamp>` attribute,
  never from the filename.
- `rerun_index` stays `None` until `pytest-rerunfailures` is adopted — no
  approximation.
- `logs/` and `reports/` are separate, uncoupled, and gitignored.
- `resource/archive/` (legacy AD code) is reference only — not migrated, not run.
- Python 3.10+ (`str | None` hints); dataclasses for typed models.
