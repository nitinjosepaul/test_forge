"""
framework
=========

The Flaky Test Detector core. This package analyzes historical pytest JUnit
XML reports and classifies each test as Stable, Suspect, or Flaky.

It has no dependency on pytest itself and no dependency on any test plugin
(``resource/``, ``plugins/``) — it only ever reads JUnit XML files from
disk. See the project README / plan.md "Flaky Test Detector Specification"
section for the full pipeline design.
"""
