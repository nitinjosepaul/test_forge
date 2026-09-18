================================================================================
TEST FORGE — FLAKY TEST DETECTOR & AUTOMATION POC
================================================================================

OVERVIEW
--------------------------------------------------------------------------------
test_forge originated as a Python/Tkinter Active Directory testing tool. It is
being repurposed into a pytest-first automation framework built around a
single, focused objective:

    Design and implement a deterministic Flaky Test Detector that analyzes
    historical pytest runs and classifies each test as Stable, Suspect, or
    Flaky — backed by a real plugin-based test suite and a CI pipeline built
    from scratch in GitHub Actions.

This is a personal learning project intended to rebuild Python fluency and
produce an interview-ready portfolio piece for Automation Engineer / SDET
roles. Secondary goals — light API automation and DB validation — are
included but deliberately scoped down in favor of depth on the detector and
CI/CD.

Legacy AD code under `library/` is out of scope going forward. It is excluded
from pytest discovery and retained only until it is deleted; it will not be
migrated or converted into a plugin.

SCOPE
--------------------------------------------------------------------------------
  In focus          pytest framework/plugin architecture, flaky test
                     analytics, GitHub Actions CI/CD (new skill area)
  Included, light    API automation, DB validation
  Out of scope       heavy UI automation, deep DB engineering, AD/Tkinter code

TIMELINE
--------------------------------------------------------------------------------
~3.5 months across 8 sprints (2 weeks / 10 story points each). Sprint sizing
is intentionally conservative to leave room for day-to-day work commitments
and mid-course adjustments.

PRIORITY ORDER
--------------------------------------------------------------------------------
  1. Minimal pytest foundation
  2. Convert the existing Selenium POM code into plugins/selenium_pom
     (the only active plugin initially)
  3. Design real + engineered flakiness into that plugin
  4. Learn GitHub Actions; generate 15-20 historical JUnit runs via a
     matrix workflow
  5. Build the flaky detector (normalize -> classify -> impact -> report)
  6. Wire the detector into CI as a quality gate
  7. Add light API automation
  8. Add light DB validation
  9. Harden, document, and prepare the showcase/demo

ARCHITECTURE
--------------------------------------------------------------------------------
    test_forge/
      |-- pyproject.toml / pytest.ini      testpaths excludes library/ (AD code)
      |-- conftest.py                      root fixtures, artifact path, run metadata
      |-- core/
      |   `-- util/log_manager.py          shared logging infra
      |-- framework/                       the flaky detector
      |   |-- normalize.py                 JUnit XML ingestion
      |   |-- classify.py                  flaky rules + confidence
      |   |-- impact.py                    suite gate logic
      |   |-- reporting.py                 JSON / CSV / HTML output
      |   |-- cli.py                       analysis entry point
      |   `-- ai_summary.py (optional)     narrative overlay only, no gate authority
      |-- plugins/
      |   |-- selenium_pom/                converted from resource/page_object_model
      |   |-- api_plugin/                  added in Sprint 6
      |   `-- db_validation/               added in Sprint 7
      |-- artifacts/pytest-runs/           15-20 JUnit XML reports from GitHub Actions
      `-- .github/workflows/
          |-- generate-history.yml         matrix run -> N JUnit artifacts -> aggregated
          `-- flaky-gate.yml               runs framework.cli, enforces the gate

    library/  (legacy AD code, excluded from discovery, pending deletion)

KEY DESIGN DECISIONS
--------------------------------------------------------------------------------
pytest is the sole execution engine. `core/` holds framework-agnostic shared
infra (currently just logging); `framework/` is the detector and never
imports from a plugin; each plugin under `plugins/` owns its own
`conftest.py` and fixtures.

  - AD code (library/) — excluded from discovery only, not migrated, not a
    plugin. Left in place until deleted.
  - Only one plugin exists early on — plugins/selenium_pom, converted from
    resource/page_object_model. api_plugin and db_validation are scaffolded
    only in their own sprints (6 and 7).
  - Logging — LogManager (from the POM utilities) is promoted to
    core/util/log_manager.py, replacing library/util/log.py.
  - Flakiness is both real and engineered:
      * Real: 1-2 existing Selenium steps are left genuinely timing-sensitive
        (e.g. no explicit wait) to produce authentic intermittent failures.
      * Engineered: 2-3 dummy tests use controlled randomness or sleep-based
        races, clearly commented as intentional, guaranteeing all three
        labels (Stable / Suspect / Flaky) appear reliably in a demo.
  - History generation target — 15-20 runs. Enough for meaningful fail-rate
    and trend math without a long generation cycle.
  - History generation mechanism — a GitHub Actions matrix workflow
    (generate-history.yml) spins up N jobs, each running the selenium_pom
    suite once and uploading its own junit-<run>.xml; an aggregation job
    downloads all artifacts into artifacts/pytest-runs/. This workflow
    doubles as the vehicle for learning GitHub Actions itself — no prior
    CI/CD experience is assumed.
  - API automation (Sprint 6) — a lightweight requests.Session client,
    auth coverage, and a handful of CRUD/negative-path tests. Target API
    and auth mechanism are locked at the start of the sprint.
  - DB validation (Sprint 7) — a thin helper layer (select / insert-update
    verification / state checks), used mainly to confirm API-driven effects.
    SQLite is the working default; engine choice is locked at the start of
    the sprint.

FLAKY TEST DETECTOR SPECIFICATION
--------------------------------------------------------------------------------
Problem
    Unstable tests create noisy failures, rerun waste, and low trust in CI
    results. Standard pass/fail reporting gives no signal to act on.

Problem statement
    Analyze the last N pytest reports and classify each test as Stable,
    Suspect, or Flaky using deterministic rules over failure rate, rerun
    recovery behavior, and failure signature variance.

Locked scope boundaries
    - Input: last N pytest reports (JUnit XML + optional pytest metadata)
    - No multi-framework ingestion in MVP
    - No mandatory AI for classification in MVP
    - Output: suite summary + per-test ranked insights + CI gate signal

Why this scope
    Architecture-heavy but achievable; directly useful in real CI pipelines
    with minimal framework disruption; strong interview narrative around
    signal quality, governance, and quality gates.

Data flow
    Last N Pytest Reports -> Ingestion -> Normalization -> Feature
    Extraction -> Rule Engine + Scoring -> Impact + Gate -> Reports + CI
    Artifacts

Output model
    1. Suite Summary — total tests, stable/suspect/flaky counts, overall
       flakiness score, trend vs previous window
    2. Ranked Test Table — test_id, label, fail_rate, rerun_recovery,
       signature_count, confidence
    3. Per-Test Drilldown — recent run timeline, top signatures, suggested
       next action

Module skeletons

    # framework/normalize.py
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
        def parse_junit(self, xml_path: str) -> list[TestRunRecord]: ...
        def normalize(self, records: list[TestRunRecord]) -> list[TestRunRecord]: ...

    # framework/classify.py
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
        def build(self, records) -> list[TestFeatures]: ...

    class RuleEngine:
        def classify(self, f: TestFeatures) -> Classification: ...

    # framework/impact.py
    @dataclass
    class SuiteImpact:
        total_tests: int
        flaky_count: int
        suspect_count: int
        flakiness_score: float
        gate: str
        rationale: str

    class ImpactEvaluator:
        def evaluate(self, classifications) -> SuiteImpact: ...

Topics covered
    module boundaries & clean interfaces · dataclasses for typed models ·
    deterministic rule engine design · JUnit XML structure & parsing ·
    rerun metadata conventions · stable test ID construction · fail rate &
    moving windows · signature variance & trend heuristics · confidence
    scoring & conflict handling · threshold policies & gate semantics ·
    artifact publishing & traceability · non-blocking AI summarization

SPRINT PLAN
--------------------------------------------------------------------------------
Full task-by-task breakdown with story points lives in resource/sprints/,
one file per sprint, formatted for direct import into JIRA:

    sprint-1-pytest-foundation.txt
    sprint-2-pom-plugin-flakiness.txt
    sprint-3-github-actions-history.txt
    sprint-4-detector-normalize-classify.txt
    sprint-5-detector-impact-report-cli-gate.txt
    sprint-6-api-automation-light.txt
    sprint-7-db-validation-light.txt
    sprint-8-hardening-showcase.txt

DELIVERABLES
--------------------------------------------------------------------------------
  - A runnable pytest framework with clean plugin boundaries
  - A Selenium POM plugin producing real and engineered flaky signal
  - A GitHub Actions history-generation workflow (first CI/CD project)
  - A working flaky test detector (normalize/classify/impact/report/CLI)
    driven by real JUnit history
  - A CI gate workflow enforcing the detector's PASS/WARN/FAIL decision
  - A small, real API automation slice and DB validation slice
  - Interview-ready documentation, architecture diagram, and demo script

NOTES
--------------------------------------------------------------------------------
Deterministic outputs — labels, confidence, and the CI gate — remain the
source of truth throughout. AI summarization is optional, additive, and
never influences classification or gate decisions.

================================================================================
