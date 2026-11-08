"""Lab 6 - Code (line) coverage tests for password_policy.py"""
import pytest
from password_policy import check_password, strength, suggest_fix


# ---------- check_password ----------
def test_valid_password_has_no_issues():
    assert check_password("Abcdef1!") == []


def test_too_short():
    assert "too short" in check_password("Ab1!")


def test_too_long():
    assert "too long" in check_password("Aa1!" + "x" * 70)


def test_common_password():
    assert "common" in check_password("password")


def test_missing_uppercase():
    assert "no uppercase" in check_password("abcdef1!")


def test_missing_lowercase():
    assert "no lowercase" in check_password("ABCDEF1!")


def test_missing_digit():
    assert "no digit" in check_password("Abcdefg!")


def test_missing_special():
    assert "no special" in check_password("Abcdefg1")


# ---------- strength ----------
def test_valid_password_is_good():
    assert strength("Abcdef1!") == "good"


def test_strong_password():
    assert strength("Abcdefghijkl1!") == "strong"


def test_weak_password():
    assert strength("Abcdefg1") == "weak"          # only "no special"


def test_very_weak_password():
    assert strength("abc") == "very weak"          # many issues


# ---------- suggest_fix ----------
def test_suggest_none_needed():
    assert suggest_fix([]) == "none needed"


def test_suggest_too_short():
    assert suggest_fix(["too short"]) == "add more characters"


def test_suggest_common():
    assert suggest_fix(["common"]) == "avoid common passwords"


def test_suggest_missing_class():
    assert suggest_fix(["no digit"]) == "add digit"


def test_suggest_too_long():
    assert suggest_fix(["too long"]) == "shorten it"
