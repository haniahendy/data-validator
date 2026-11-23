"""A tiny declarative DataFrame validator (schema, ranges, uniqueness, allowed values, nulls)."""
from dataclasses import dataclass, field

import pandas as pd


@dataclass
class Column:
    name: str
    dtype: str | None = None          # "int", "float", "str", "datetime"
    nullable: bool = True
    unique: bool = False
    min: float | None = None
    max: float | None = None
    allowed: set | None = None


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


_KIND = {"int": "iu", "float": "iuf", "str": "O", "datetime": "M"}


def validate(df: pd.DataFrame, schema: list[Column]) -> Report:
    rep = Report()
    for c in schema:
        if c.name not in df.columns:
            rep.errors.append(f"{c.name}: column missing")
            continue
        s = df[c.name]
        if c.dtype and s.dtype.kind not in _KIND[c.dtype]:
            rep.errors.append(f"{c.name}: expected {c.dtype}, got {s.dtype}")
            continue
        if not c.nullable and s.isna().any():
            rep.errors.append(f"{c.name}: {int(s.isna().sum())} null value(s)")
        if c.unique and s.dropna().duplicated().any():
            rep.errors.append(f"{c.name}: duplicate values")
        if c.min is not None and (s.dropna() < c.min).any():
            rep.errors.append(f"{c.name}: {int((s.dropna() < c.min).sum())} value(s) below {c.min}")
        if c.max is not None and (s.dropna() > c.max).any():
            rep.errors.append(f"{c.name}: {int((s.dropna() > c.max).sum())} value(s) above {c.max}")
        if c.allowed is not None:
            bad = ~s.dropna().isin(c.allowed)
            if bad.any():
                rep.errors.append(f"{c.name}: {int(bad.sum())} value(s) not in allowed set")
    return rep
