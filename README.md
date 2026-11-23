# data-validator

A small declarative data-validation library for pandas DataFrames: describe each column (type, nullable, unique, min/max, allowed values) and get a readable list of errors. Written to practice API design and test-first development, not to replace tools like Great Expectations or pandera.

```python
from validator.core import Column, validate
schema = [Column("id", "int", nullable=False, unique=True), Column("age", "int", min=0, max=120)]
report = validate(df, schema)
print(report.ok, report.errors)
```

## Run tests
```bash
pip install -r requirements.txt
python -m pytest -q    # 4 tests
```

## Limits
No cross-column rules, no regex checks, no custom messages, whole-frame operations only (not designed for very large data). Type check is by numpy dtype kind.

## Provenance
A learning and portfolio project.
