"""Lab 6 - Branch coverage tests for password_policy.py

Every decision is exercised both True and False, including the
loop-entry / loop-exit branches of the character-classification loop.
"""
import pytest
from password_policy import check_password, strength, suggest_fix, COMMON


# ---------- check_password: length if / elif / neither ----------
def test_valid_password_has_no_issues():
    assert check_password("Abcdef1!") == []


@pytest.mark.parametrize("pw", ["Ab1!", "Abcdef1"])          # 4 and 7 chars
def test_too_short(pw):
    assert "too short" in check_password(pw)


def test_boundary_8_chars_not_short():
    assert "too short" not in check_password("Abcdef1!")


def test_boundary_64_chars_not_too_long():
    pw = "Aa1!" + "x" * 60
    assert len(pw) == 64
    assert check_password(pw) == []


def test_boundary_65_chars_too_long():
    pw = "Aa1!" + "x" * 61
    assert len(pw) == 65
    assert check_password(pw) == ["too long"]


# ---------- common-password check True / False ----------
@pytest.mark.parametrize("pw", sorted(COMMON) + ["PASSWORD", "QwErTy"])
def test_common_passwords_flagged(pw):
    assert "common" in check_password(pw)


def test_non_common_not_flagged():
    assert "common" not in check_password("Abcdef1!")


# ---------- character classification loop (each elif both ways) ----------
def test_empty_string_skips_loop():
    issues = check_password("")
    assert issues == ["too short", "no uppercase", "no lowercase",
                      "no digit", "no special"]


def test_all_character_types_present():
    assert check_password("Aa1!Aa1!") == []


def test_missing_uppercase():
    assert check_password("abcdef1!") == ["no uppercase"]


def test_missing_lowercase():
    assert check_password("ABCDEF1!") == ["no lowercase"]


def test_missing_digit():
    assert check_password("Abcdefg!") == ["no digit"]


def test_missing_special():
    assert check_password("Abcdefg1") == ["no special"]


def test_space_counts_as_special():
    assert "no special" not in check_password("Abcdef 1")


# ---------- strength: all four outcomes + both inner-if sides ----------
def test_strength_good():
    assert strength("Abcdef1!") == "good"


def test_strength_good_boundary_13_chars():
    pw = "Abcdefghijk1!"
    assert len(pw) == 13
    assert strength(pw) == "good"


def test_strength_strong_boundary_14_chars():
    pw = "Abcdefghijkl1!"
    assert len(pw) == 14
    assert strength(pw) == "strong"


def test_strength_weak_one_issue():
    assert strength("Abcdefg1") == "weak"


def test_strength_weak_exactly_two_issues():
    assert len(check_password("abcdefg1")) == 2          # upper + special
    assert strength("abcdefg1") == "weak"


def test_strength_very_weak_three_issues():
    assert len(check_password("abcdefgh")) == 3          # upper, digit, special
    assert strength("abcdefgh") == "very weak"


# ---------- suggest_fix: every if both ways ----------
def test_suggest_none_needed():
    assert suggest_fix([]) == "none needed"


def test_suggest_too_short():
    assert suggest_fix(["too short"]) == "add more characters"


def test_suggest_common():
    assert suggest_fix(["common"]) == "avoid common passwords"


@pytest.mark.parametrize("issue, expected", [
    ("no uppercase", "add uppercase"),
    ("no lowercase", "add lowercase"),
    ("no digit", "add digit"),
    ("no special", "add special"),
])
def test_suggest_missing_class(issue, expected):
    assert suggest_fix([issue]) == expected


def test_suggest_too_long_falls_through():
    assert suggest_fix(["too long"]) == "shorten it"


def test_suggest_uses_only_first_issue():
    assert suggest_fix(["too short", "no digit"]) == "add more characters"
