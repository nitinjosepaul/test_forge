================================================================================
TEST FORGE — FLAKY TEST DETECTOR + AUTOMATION POC
================================================================================

WHAT THIS PROJECT IS NOW
================================================================================
test_forge started as a Python/Tkinter Active Directory testing framework.
It is being repurposed into a pytest-first automation + analytics POC whose
primary goal is:

  1. Rebuild deep Python fluency
  2. Build a deterministic Flaky Test Detector (the core differentiator)
  3. Learn GitHub Actions from scratch and use it to generate real test
     run history
  4. Add light API automation and DB validation later
  5. Produce an interview-ready portfolio piece (architecture + demo + docs)

The old AD/Tkinter code under `library/` is NOT part of this direction. It is
excluded from pytest discovery and left in place only until it is deleted.
It is not migrated, not turned into a plugin, and not maintained further.

================================================================================
GOAL
================================================================================
Rebuild Python fluency and interview readiness through a final, focused
attempt built around:
  - a pytest-first plugin framework
  - the Selenium POM plugin as the sole active test source (used to generate
    real + engineered flaky signal)
  - GitHub Actions learned from scratch, used to generate run history and
    later to gate the pipeline
  - a deterministic flaky test detector as the primary differentiator
  - API automation and DB validation added later, deliberately kept light

================================================================================
TIMELINE
================================================================================
~3.5 months total: 8 sprints x 2 weeks x 10 story points per sprint.

10 points/sprint (not 14) is a deliberate choice to leave breathing room for
pending work, leave days, and mid-course clarification — this is meant to be
sustainable, not packed to full capacity.

================================================================================
PRIORITY ORDER (FINALIZED)
================================================================================
1. Minimal pytest foundation (just enough to run something real)
2. Convert resource/page_object_model into plugins/selenium_pom/
   (the only active plugin initially)
3. Design real + engineered flakiness into that plugin
4. Learn GitHub Actions and use it to generate 15-20 historical JUnit runs
5. Build the flaky detector (normalize -> classify -> impact -> report)
   against real accumulated history
6. Wire the detector into CI as a gate
7. Add API automation (light)
8. Add DB validation (light)
9. Harden, document, and prepare the showcase/demo

================================================================================
SCOPE
================================================================================
Core:                 pytest framework architecture, fixtures, hooks,
                       logging, artifacts
Primary learning:      Python fluency, framework/plugin design, flaky test
                       analytics, GitHub Actions (new skill)
Secondary (light):     API automation and DB validation, deliberately shallow
Detector data source:  Selenium POM plugin only — no AD plugin, no separate
                       dummy-only harness
Not the focus:         heavy UI automation, deep DB framework engineering,
                       or migrating/preserving AD code

================================================================================
KEY DECISIONS LOCKED IN
================================================================================
- AD code (library/) is not migrated and not a plugin. It is simply excluded
  from pytest discovery (via testpaths) and left as dead code to be deleted
  later. No sprint time is spent on it.
- Only one plugin exists early on: plugins/selenium_pom/, converted from
  resource/page_object_model. api_plugin and db_validation are not
  scaffolded until their own sprints (6 and 7).
- Flakiness is both real and engineered:
    * Real: 1-2 existing Selenium steps are deliberately left
      timing-sensitive (e.g. no explicit wait) so genuine intermittent
      failures occur across runs.
    * Engineered: 2-3 small dummy tests use controlled randomness or
      sleep-based races, clearly commented as intentional, to guarantee all
      three labels (Stable/Suspect/Flaky) show up reliably in a demo.
- History generation target: 15-20 historical runs, no more — enough for
  meaningful fail-rate/trend math without taking long to generate.
- History generation mechanism: a GitHub Actions workflow using a matrix
  strategy — one workflow run spins up N matrix jobs, each executing the
  selenium_pom suite once and uploading its own junit-<run>.xml artifact. An
  aggregation job then downloads all matrix artifacts and bundles them into
  artifacts/pytest-runs/ for the detector to consume. This workflow is also
  the vehicle for learning GitHub Actions itself.
- CI experience assumption: no prior GitHub Actions experience — the plan
  budgets explicit time to learn the fundamentals rather than assuming
  familiarity.

================================================================================
ARCHITECTURE
================================================================================
test_forge/
  |-- pyproject.toml / pytest.ini         <- testpaths excludes library/ (AD code)
  |-- conftest.py                         <- root fixtures, artifact path, run metadata
  |-- core/
  |   `-- util/
  |       `-- log_manager.py              <- shared logging infra
  |-- framework/
  |   |-- normalize.py                    <- JUnit XML ingestion
  |   |-- classify.py                     <- flaky rules + confidence
  |   |-- impact.py                       <- suite gate logic
  |   |-- reporting.py                    <- JSON/CSV/HTML outputs
  |   |-- cli.py                          <- analysis entry point
  |   `-- ai_summary.py (optional)        <- narrative overlay only
  |-- plugins/
  |   |-- selenium_pom/                   <- converted from resource/page_object_model
  |   |                                      (sole active plugin early on)
  |   |-- api_plugin/                     <- added later (Sprint 6)
  |   `-- db_validation/                  <- added later (Sprint 7)
  |-- artifacts/
  |   `-- pytest-runs/                    <- 15-20 JUnit XML reports from GitHub Actions
  `-- .github/
      `-- workflows/
          |-- generate-history.yml        <- matrix workflow: N runs -> N JUnit artifacts -> aggregated
          `-- flaky-gate.yml              <- runs framework.cli against history, enforces gate

  library/  (AD code) -- excluded from pytest discovery, kept only until deletion.

================================================================================
TECHNICAL DIRECTION
================================================================================

PYTEST CORE
- pytest is the only execution engine.
- Root conftest.py owns shared fixtures: run_id, artifact directory, session
  logger, environment selection.
- Plugin-local conftest.py for domain fixtures: Selenium driver fixture
  first (only plugin fixture needed initially); API client/DB connection
  fixtures added later.
- Use pytest hooks for run metadata: pytest_addoption, pytest_configure,
  pytest_collection_modifyitems, pytest_runtest_makereport,
  pytest_sessionfinish.
- Standardize output using --junitxml and a small metadata sidecar.
- testpaths explicitly points at plugins/ and framework/ tests only —
  library/ (AD code) is never discovered.

CORE
- Promote LogManager into core/util/log_manager.py.
- Keep core reusable and framework-agnostic — shared infra only, not
  automation business logic.

FRAMEWORK (the flaky detector)
- normalize.py: parse last N JUnit XML reports into canonical run records.
- classify.py: compute fail rate, rerun recovery, signature variance, trend.
- impact.py: convert classifications into suite score and PASS/WARN/FAIL gate.
- reporting.py: generate JSON/CSV/HTML outputs.
- cli.py: single command to run the analysis pipeline.
- ai_summary.py: optional narrative layer only; no gate authority.

PLUGINS
- selenium_pom: converted from resource/page_object_model; the only plugin
  built early. Carries real (timing-sensitive) and engineered (randomized/
  sleep-based) flaky tests to generate meaningful detector input.
- api_plugin: added in Sprint 6, practical API coverage, kept simple.
- db_validation: added in Sprint 7, small DB assertion layer.
- AD code (library/): not a plugin — excluded from discovery, left for
  eventual deletion.

GITHUB ACTIONS (new skill area)
- generate-history.yml: matrix strategy job (run: [1..N], N = 15-20), each
  matrix job executes pytest plugins/selenium_pom/tests once and uploads its
  own junit-<run>.xml artifact; an aggregation job downloads all matrix
  artifacts and writes them into artifacts/pytest-runs/.
- flaky-gate.yml: separate, simpler workflow added once the detector CLI
  exists — reads accumulated history, runs framework.cli, and fails/warns
  the workflow based on the suite gate.
- Learning scope: triggers (workflow_dispatch, push), jobs/steps, matrix
  strategy, artifact upload/download, job summaries — treated as genuinely
  new material, not assumed knowledge.

================================================================================
MODULE-LEVEL IMPLEMENTATION DETAILS
================================================================================

LOGGING
- Replace library/util/log.py with core/util/log_manager.py.
- Use named handlers with add/remove lifecycle.
- Keep file logging and console logging separate.
- Make logging usable from pytest fixtures and plugin code.

SELENIUM POM PLUGIN (built first)
- Move resource/page_object_model/{base,pages,workflows,tests} into
  plugins/selenium_pom/.
- Fix all import paths and add a plugin-local conftest.py (driver fixture,
  browser option).
- Verify all existing POM tests still pass after the move before adding
  anything new.

DESIGNING FLAKINESS (real + engineered)
- Real flakiness: identify 1-2 existing steps with weak/missing explicit
  waits and leave them as-is (or slightly loosen a wait) so genuine
  timing-based intermittent failures occur across repeated runs.
- Engineered flakiness: add 2-3 small, clearly commented dummy tests that
  fail based on controlled randomness (e.g. random.random() < 0.3) or
  artificial sleep-based races, so the demo reliably produces all three
  labels regardless of what the real UI does.
- Keep both kinds clearly distinguishable in code/comments so the interview
  story is honest: "this one is real timing flakiness, this one is
  intentionally engineered to demonstrate the classifier."

GITHUB ACTIONS (learned as part of this POC)
- Start with fundamentals: workflow YAML structure, triggers, jobs, steps,
  actions/upload-artifact / actions/download-artifact.
- Build generate-history.yml using a matrix strategy
  (strategy.matrix.run: [1..N]) so one workflow execution produces N
  independent JUnit XML artifacts (N = 15-20).
- Add an aggregation job that depends on the matrix job, downloads all
  artifacts, and writes them into artifacts/pytest-runs/.
- Later, add flaky-gate.yml to run framework.cli against the aggregated
  history and enforce PASS/WARN/FAIL as a workflow outcome.

API AUTOMATION (deferred to Sprint 6, kept light)
- Use a lightweight client wrapper over requests.Session.
- Cover auth/login, simple CRUD, negative-path checks, response validation.
- Keep assertions readable and reusable. Avoid overbuilding a full API
  framework.
- Target API and auth mechanism to be explicitly locked at the start of
  Sprint 6, not assumed in advance.

DB VALIDATION (deferred to Sprint 7, kept light)
- Keep DB validation simple and targeted.
- Build helpers for select, insert/update verification, row count/state
  checks.
- Use it mainly to confirm API effects or setup/cleanup state.
- DB engine choice (SQLite recommended) to be explicitly locked at the
  start of Sprint 7.

FLAKY DETECTOR
- Input: last N (15-20) JUnit XML reports generated via generate-history.yml.
- Output: Stable / Suspect / Flaky
- Deterministic signals: fail rate, rerun recovery, signature count/variance,
  recent streak, short-term trend.
- Keep labels and gates explainable.

================================================================================
FLAKY TEST DETECTOR SPECIFICATION
================================================================================

PROBLEM
Unstable tests create noisy failures, rerun waste, and low trust in CI
results. Standard pass/fail reporting does not give enough signal to act on
instability.

FINAL PROBLEM STATEMENT
Design and implement a Python-based flaky test detector that analyzes the
last N pytest reports and classifies each test as Stable, Suspect, or Flaky
using deterministic rules over failure rate, rerun recovery behavior, and
failure signature variance.

LOCKED SCOPE BOUNDARIES
- Input source: last N pytest result reports (JUnit XML + optional pytest
  metadata)
- No multi-framework ingestion in MVP
- No mandatory AI for classification in MVP
- Output: suite summary + per-test ranked insights + CI gate signal

WHY THIS SCOPE
- Simpler than a full distributed validation platform, but still
  architecture-heavy.
- Directly useful in real CI pipelines with minimal framework disruption.
- Strong Staff SDET interview narrative: signal quality, governance, and
  quality gates.

PROPOSED POC
Build a reusable framework with:
- report ingestion and run-history store
- feature extraction (fail rate, rerun recovery, signature variance, trend)
- deterministic rule engine for Stable/Suspect/Flaky classification
- confidence and risk scoring
- report generation (JSON, CSV, HTML summary)
- CI quality gates (warn/fail thresholds)
- optional AI summarization assistant (non-blocking, post-classification)

DATA FLOW
Last N Pytest Reports -> Ingestion Layer -> Normalization Layer ->
Feature Extraction -> Rule Engine + Scoring -> Impact + Gate ->
Reports + CI Artifacts

OUTPUT MODEL
1. Suite Summary
   - total tests, stable/suspect/flaky counts
   - overall flakiness score
   - trend vs previous window
2. Ranked Test Table
   - test_id, label, fail_rate, rerun_recovery, signature_count, confidence
3. Per-Test Drilldown
   - recent run timeline, top signatures, suggested next action

BASE MODULE SKELETONS

framework.normalize
--------------------
Purpose: parse pytest reports and map to a canonical model.

    from dataclasses import dataclass

    @dataclass
    class TestRunRecord:
        run_id: str
        test_id: str
        status: str
        duration_ms: int
        failure_signature: str | None
        rerun_index: int | None
        timestamp_utc: str

    class ReportNormalizer:
        def parse_junit(self, xml_path: str) -> list[TestRunRecord]:
            ...

        def normalize(self, records: list[TestRunRecord]) -> list[TestRunRecord]:
            # cleanup IDs, normalize status values, dedupe
            ...

framework.classify
--------------------
Purpose: derive features and classify Stable/Suspect/Flaky with confidence.

    from dataclasses import dataclass

    @dataclass
    class TestFeatures:
        test_id: str
        fail_rate: float
        rerun_recovery_rate: float
        signature_count: int
        recent_fail_streak: int

    @dataclass
    class Classification:
        test_id: str
        label: str
        confidence: float
        reasons: list[str]

    class FeatureExtractor:
        def build(self, records) -> list[TestFeatures]:
            ...

    class RuleEngine:
        def classify(self, f: TestFeatures) -> Classification:
            ...

framework.impact
--------------------
Purpose: convert per-test results into suite risk and CI gate decision.

    from dataclasses import dataclass

    @dataclass
    class SuiteImpact:
        total_tests: int
        flaky_count: int
        suspect_count: int
        flakiness_score: float
        gate: str
        rationale: str

    class ImpactEvaluator:
        def evaluate(self, classifications) -> SuiteImpact:
            ...

TOPICS TO COVER
- module boundaries and clean interfaces
- dataclasses for typed models
- deterministic rule engine design
- JUnit XML structure and parsing
- rerun metadata conventions
- stable test ID construction
- fail rate and moving windows
- signature variance and trend heuristics
- confidence scoring and conflict handling
- threshold policies and gate semantics
- artifact publishing and traceability
- AI summaries that do not affect gate decisions

================================================================================
8-SPRINT PLAN (10 POINTS PER SPRINT, 2 WEEKS EACH, ~3.5 MONTHS TOTAL)
================================================================================
Full task-by-task breakdown with story points lives in:
  resource/sprints/sprint-1-pytest-foundation.txt
  resource/sprints/sprint-2-pom-plugin-flakiness.txt
  resource/sprints/sprint-3-github-actions-history.txt
  resource/sprints/sprint-4-detector-normalize-classify.txt
  resource/sprints/sprint-5-detector-impact-report-cli-gate.txt
  resource/sprints/sprint-6-api-automation-light.txt
  resource/sprints/sprint-7-db-validation-light.txt
  resource/sprints/sprint-8-hardening-showcase.txt

These files are formatted for direct import into JIRA (short description +
a numbered task list with story points per task).

================================================================================
DELIVERABLES
================================================================================
- A runnable pytest framework with clean plugin boundaries
- One fully working Selenium POM plugin generating real and engineered
  flaky signal
- A GitHub Actions history-generation workflow (first real CI project)
- A working flaky test detector (normalize/classify/impact/report/CLI) over
  real JUnit history
- A CI gate workflow enforcing the detector's PASS/WARN/FAIL decision
- A small but real API automation slice (added later, Sprint 6)
- A small DB validation slice (added later, Sprint 7)
- Interview-friendly documentation, architecture diagram, and demo script

================================================================================
KEY NOTES
================================================================================
- This is a final attempt to regain automation fluency and interview
  readiness — the timeline (~3.5 months, 10 points/sprint) is deliberately
  conservative to leave room for pending work, leaves, and mid-course
  clarification.
- The flaky detector, its Selenium POM data source, and GitHub Actions are
  the priority path — everything else is sequenced around them.
- AD code is excluded from discovery, not migrated or preserved as a plugin.
- API and DB automation are real but intentionally light, and deliberately
  scheduled last.
- Deterministic outputs (labels, confidence, gate) remain the source of
  truth; AI stays non-blocking and additive only.

================================================================================
