"""Flaky synthetic tests — controlled ~40-50% fail rate. A couple of tests
deliberately vary their failure signature (different exception types and
messages across runs) to demonstrate signature-variance detection. Used to
demonstrate the 'Flaky' label.

No Selenium/browser dependency; failure rate is driven by controlled
randomness (no fixed seed) so behavior varies naturally across repeated
pytest invocations.
"""
import random


def test_flaky_case_1():
    roll = random.random()
    assert roll > 0.45, f"Flaky failure simulated (roll={roll:.3f})"


def test_flaky_case_2():
    roll = random.random()
    assert roll > 0.45, f"Flaky failure simulated (roll={roll:.3f})"


def test_flaky_case_3():
    # Deliberately varies its failure signature across runs.
    roll = random.random()
    if roll <= 0.25:
        raise ValueError(f"Simulated timeout error (roll={roll:.3f})")
    if roll <= 0.5:
        raise AssertionError(f"Simulated state mismatch (roll={roll:.3f})")
    assert True


def test_flaky_case_4():
    roll = random.random()
    assert roll > 0.5, f"Flaky failure simulated (roll={roll:.3f})"


def test_flaky_case_5():
    roll = random.random()
    assert roll > 0.4, f"Flaky failure simulated (roll={roll:.3f})"


def test_flaky_case_6():
    # Deliberately varies its failure signature across runs.
    roll = random.random()
    if roll <= 0.2:
        raise ConnectionError(f"Simulated connection drop (roll={roll:.3f})")
    if roll <= 0.45:
        raise AssertionError(f"Simulated data drift (roll={roll:.3f})")
    assert True


def test_flaky_case_7():
    roll = random.random()
    assert roll > 0.48, f"Flaky failure simulated (roll={roll:.3f})"


def test_flaky_case_8():
    roll = random.random()
    assert roll > 0.42, f"Flaky failure simulated (roll={roll:.3f})"


def test_flaky_case_9():
    roll = random.random()
    assert roll > 0.5, f"Flaky failure simulated (roll={roll:.3f})"


def test_flaky_case_10():
    roll = random.random()
    assert roll > 0.4, f"Flaky failure simulated (roll={roll:.3f})"
