"""Stable synthetic tests — always pass. Used to demonstrate the 'Stable' label.

These tests carry no Selenium/browser dependency; they exist purely to
generate reliable, always-green signal for the flaky test detector demo.
"""


def test_stable_case_1():
    assert 2 + 2 == 4


def test_stable_case_2():
    assert "hello".upper() == "HELLO"


def test_stable_case_3():
    assert sorted([3, 1, 2]) == [1, 2, 3]


def test_stable_case_4():
    assert len("test_forge") == 10


def test_stable_case_5():
    assert True


def test_stable_case_6():
    assert {"a": 1}.get("a") == 1


def test_stable_case_7():
    assert [1, 2, 3][-1] == 3


def test_stable_case_8():
    assert (1, 2) == (1, 2)


def test_stable_case_9():
    assert "abc" in "xabcx"


def test_stable_case_10():
    assert round(3.14159, 2) == 3.14
