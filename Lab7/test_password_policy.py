from hypothesis import given, strategies as st
from password_policy import (
    first_character_type,
    split_credentials,
    digit_ratio
)


@given(st.one_of(st.text(), st.none()))
def test_first_character_type_no_crash(s):
    result = first_character_type(s)

    if not s:
        assert result is None


@given(st.one_of(st.text(), st.none()))
def test_split_credentials_no_crash(s):
    result = split_credentials(s)

    if s is None or s.count(":") != 1:
        assert result is None


@given(st.one_of(st.text(), st.none()))
def test_digit_ratio_no_crash(s):
    result = digit_ratio(s)

    if not s:
        assert result == 0.0