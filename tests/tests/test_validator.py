import pandas as pd

from validator.core import Column, validate

SCHEMA = [Column("id", "int", nullable=False, unique=True),
          Column("age", "int", min=0, max=120),
          Column("status", "str", allowed={"a", "b"})]


def good():
    return pd.DataFrame({"id": [1, 2], "age": [30, 40], "status": ["a", "b"]})


def test_valid_frame_passes():
    assert validate(good(), SCHEMA).ok


def test_missing_column():
    assert "id: column missing" in validate(good().drop(columns="id"), SCHEMA).errors


def test_wrong_dtype():
    assert any("expected int" in e for e in validate(good().assign(age=["x", "y"]), SCHEMA).errors)


def test_nulls_duplicates_ranges_allowed():
    df = pd.DataFrame({"id": [1, 1, None], "age": [-1, 200, 5], "status": ["a", "z", "b"]})
    errs = validate(df, SCHEMA).errors
    assert any("id: expected int" in e for e in errs) or any("null" in e for e in errs)
    df2 = pd.DataFrame({"id": [1, 1, 3], "age": [-1, 200, 5], "status": ["a", "z", "b"]})
    errs2 = validate(df2, SCHEMA).errors
    assert "id: duplicate values" in errs2
    assert any("below 0" in e for e in errs2) and any("above 120" in e for e in errs2)
    assert any("not in allowed set" in e for e in errs2)
