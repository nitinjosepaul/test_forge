"""
framework.normalize
====================

Stage 1 of the Flaky Test Detector pipeline: parse pytest JUnit XML reports
and map them into a canonical, framework-agnostic model (``TestRunRecord``).

This module has NO dependency on pytest itself, and NO dependency on any
plugin under ``resource/`` or ``plugins/`` — it only ever reads JUnit XML
files from disk. That keeps the detector fully decoupled from whichever test
framework/plugin produced the reports (per the locked scope boundary: JUnit
XML + optional pytest metadata only).

Pipeline entry point for callers: ``load_history(reports_dir)``.
"""
from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path


@dataclass
class TestRunRecord:
    """One canonical test execution result, for one test, in one run."""

    run_id: str
    test_id: str
    status: str                  # "passed" / "failed" / "error" / "skipped"
    duration_ms: int
    failure_signature: str | None
    rerun_index: int | None
    timestamp_utc: str


# Regex used to strip numeric literals (e.g. "roll=0.256") out of failure
# messages before treating them as a "signature". Without this, every
# synthetic failure would look like a unique signature (since our dummy
# tests embed a random float in the message), which would make
# signature_count meaningless for classification.
_NUMERIC_LITERAL_RE = re.compile(r"\d+\.\d+|\d+")


class ReportNormalizer:
    """Parses JUnit XML reports into canonical ``TestRunRecord`` objects."""

    def parse_junit(self, xml_path: str) -> list[TestRunRecord]:
        """
        Parse a single JUnit XML report into a list of TestRunRecord, one
        per <testcase> element found in the file.

        The report's <testsuite timestamp="..."> attribute is read ONCE and
        used as both `run_id` and `timestamp_utc` for every testcase in this
        file — i.e. one file == one run, all of its testcases share one
        identity. This is deliberate: filenames (run_1.xml, run_10.xml, ...)
        are purely for human/file-system convenience and carry no meaning
        for the detector. Sorting/ordering is always done on this parsed
        timestamp, never on the filename.
        """
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # pytest's --junitxml can emit either a single <testsuite> as the
        # root, or a <testsuites> wrapper containing one or more
        # <testsuite> children (this is the "xunit2" family format, which is
        # what our current pytest version produced). Handle both shapes.
        if root.tag == "testsuites":
            testsuites = root.findall("testsuite")
        elif root.tag == "testsuite":
            testsuites = [root]
        else:
            raise ValueError(
                f"Unexpected JUnit XML root element '{root.tag}' in {xml_path}"
            )

        records: list[TestRunRecord] = []
        for testsuite in testsuites:
            run_id = testsuite.get("timestamp")
            if not run_id:
                raise ValueError(
                    f"<testsuite> in {xml_path} is missing a 'timestamp' "
                    f"attribute; cannot derive run_id."
                )
            timestamp_utc = run_id  # same source value, see normalize()

            for testcase in testsuite.findall("testcase"):
                records.append(
                    self._build_record(testcase, run_id, timestamp_utc)
                )

        return records

    def _build_record(
        self, testcase: ET.Element, run_id: str, timestamp_utc: str
    ) -> TestRunRecord:
        classname = testcase.get("classname", "")
        name = testcase.get("name", "")
        test_id = f"{classname}::{name}"

        time_attr = testcase.get("time", "0")
        duration_ms = int(round(float(time_attr) * 1000))

        status, failure_signature = self._extract_status_and_signature(testcase)

        return TestRunRecord(
            run_id=run_id,
            test_id=test_id,
            status=status,
            duration_ms=duration_ms,
            failure_signature=failure_signature,
            # No rerun data yet — the current demo reports were generated
            # without pytest-rerunfailures, so every record is a single,
            # independent attempt. Revisit this once reruns are introduced.
            rerun_index=None,
            timestamp_utc=timestamp_utc,
        )

    def _extract_status_and_signature(
        self, testcase: ET.Element
    ) -> tuple[str, str | None]:
        """
        Determine a testcase's status and, if it failed/errored, its
        normalized failure signature.

        JUnit XML encodes outcome as a child element (absence of any child
        means the test passed):
            <failure message="...">...</failure>  -> status "failed"
            <error message="...">...</error>       -> status "error"
            <skipped message="..."/>               -> status "skipped"
        """
        failure = testcase.find("failure")
        if failure is not None:
            return "failed", self._build_signature(failure)

        error = testcase.find("error")
        if error is not None:
            return "error", self._build_signature(error)

        skipped = testcase.find("skipped")
        if skipped is not None:
            return "skipped", None

        return "passed", None

    def _build_signature(self, node: ET.Element) -> str:
        """
        Build a normalized failure signature from a <failure>/<error>
        element's `message` attribute, e.g.:

            "AssertionError: Flaky failure simulated (roll=0.256)"
                -> "AssertionError:Flaky failure simulated (roll=<num>)"

        Normalization keeps the exception type and message shape, but
        strips numeric literals, so tests that fail the same way every time
        (just with a different random value in the message) are recognized
        as ONE recurring signature rather than many unique ones. Tests that
        genuinely vary their failure type/message (e.g. sometimes
        ValueError, sometimes AssertionError) will still produce multiple
        distinct signatures, which is the intended signal for
        signature_count.
        """
        message = (node.get("message") or "").strip()
        first_line = message.splitlines()[0] if message else ""

        if ":" in first_line:
            exc_type, _, rest = first_line.partition(":")
            exc_type = exc_type.strip()
            rest = rest.strip()
        else:
            exc_type = first_line or "UnknownError"
            rest = ""

        normalized_rest = _NUMERIC_LITERAL_RE.sub("<num>", rest)
        return f"{exc_type}:{normalized_rest}"

    def normalize(self, records: list[TestRunRecord]) -> list[TestRunRecord]:
        """
        Apply cleanup/consistency rules to an already-parsed list of
        records:
          - lowercase/trim status values (defensive; parse_junit already
            emits canonical lowercase values, this guards against future
            parser changes or hand-built records)
          - drop exact-duplicate records (defensive; shouldn't occur from a
            single parse, but load_history() may combine multiple files)
        """
        seen: set[tuple] = set()
        normalized: list[TestRunRecord] = []

        for record in records:
            record.status = record.status.strip().lower()

            key = (
                record.run_id,
                record.test_id,
                record.status,
                record.failure_signature,
            )
            if key in seen:
                continue
            seen.add(key)
            normalized.append(record)

        return normalized

    def load_history(self, reports_dir: str) -> list[TestRunRecord]:
        """
        Load and normalize every JUnit XML report found in `reports_dir`
        (non-recursive, matches "*.xml"), returning ONE flat list of
        TestRunRecord spanning all runs, sorted chronologically by the
        timestamp parsed from each report (never by filename).

        This is the entry point Stage 2 (feature extraction) is expected to
        call — parse_junit()/normalize() are the lower-level building
        blocks used internally.
        """
        directory = Path(reports_dir)
        xml_files = sorted(directory.glob("*.xml"))
        if not xml_files:
            raise FileNotFoundError(f"No JUnit XML reports found in {reports_dir}")

        all_records: list[TestRunRecord] = []
        for xml_file in xml_files:
            all_records.extend(self.parse_junit(str(xml_file)))

        normalized = self.normalize(all_records)
        normalized.sort(key=lambda r: r.timestamp_utc)
        return normalized
