"""Suspect synthetic tests — controlled ~15-20% fail rate with a single,
consistent failure signature per test. Used to demonstrate the 'Suspect'
label (occasional failures, but not enough/severe enough to be Flaky).

No Selenium/browser dependency; failure rate is driven by controlled
randomness (no fixed seed) so behavior varies naturally across repeated
pytest invocations.
"""
import random


def test_suspect_case_1():
    roll = random.random()
    assert roll > 0.15, f"Suspect failure simulated (roll={roll:.3f})"


def test_suspect_case_2():
    roll = random.random()
    assert roll > 0.15, f"Suspect failure simulated (roll={roll:.3f})"


def test_suspect_case_3():
    roll = random.random()
    assert roll > 0.18, f"Suspect failure simulated (roll={roll:.3f})"


def test_suspect_case_4():
    roll = random.random()
    assert roll > 0.18, f"Suspect failure simulated (roll={roll:.3f})"


def test_suspect_case_5():
    roll = random.random()
    assert roll > 0.2, f"Suspect failure simulated (roll={roll:.3f})"


def test_suspect_case_6():
    roll = random.random()
    assert roll > 0.2, f"Suspect failure simulated (roll={roll:.3f})"


def test_suspect_case_7():
    roll = random.random()
    assert roll > 0.15, f"Suspect failure simulated (roll={roll:.3f})"


def test_suspect_case_8():
    roll = random.random()
    assert roll > 0.17, f"Suspect failure simulated (roll={roll:.3f})"


def test_suspect_case_9():
    roll = random.random()
    assert roll > 0.19, f"Suspect failure simulated (roll={roll:.3f})"


def test_suspect_case_10():
    roll = random.random()
    assert roll > 0.16, f"Suspect failure simulated (roll={roll:.3f})"
