---
name: tdd
description: >
  Test-driven development: write a failing test first, then implement to make it pass,
  then refactor. Trigger when: writing any new function, class, or module; when fixing
  a bug (write a test that reproduces it first); when implementing a plan step.
  Do NOT trigger for pure documentation tasks or config-only changes.
---

# Test-Driven Development

Red → Green → Refactor. In that order. Every time.

## Quick start

For any function or module you're about to write:

```bash
# 1. Write the test first (it will fail — that's correct)
# 2. Run it and confirm it fails with the right error
pytest tests/test_feature.py::test_my_function -v
# Expected: FAILED (not "module not found" — that means the path is wrong)

# 3. Write the minimal implementation to make it pass
# 4. Run again — should be GREEN
# 5. Refactor for clarity — run again to confirm still green
```

## The three rules

1. **Do not write production code unless it is to make a failing test pass.**
2. **Do not write more test code than sufficient to produce a failing test.**
3. **Do not write more production code than sufficient to make the test pass.**

These rules force small, focused changes. If you find yourself writing 100 lines of implementation to pass one test, the test is too broad.

## Test structure (AAA)

```python
def test_validates_empty_input():
    # Arrange
    validator = InputValidator()
    empty_input = ""

    # Act
    result = validator.validate(empty_input)

    # Assert
    assert result.is_valid == False
    assert result.error == "Input cannot be empty"
```

Arrange: set up state.
Act: call the thing being tested.
Assert: check exactly one behavior.

## What makes a good test

✅ Tests one behavior (not one function — one behavior)
✅ Has a descriptive name: `test_raises_error_when_token_expired`
✅ Is deterministic (same result every run)
✅ Is independent (doesn't depend on order or other tests)
✅ Runs fast (< 100ms for unit tests)
✅ Fails for the right reason when the behavior breaks

❌ Tests multiple behaviors in one test
❌ Named `test_thing` or `test_1`
❌ Depends on external services (mock them)
❌ Uses `time.sleep()` to wait for async work
❌ Passes even when the code is wrong

## Fixtures and setup

Use fixtures for shared state. Don't repeat setup code in tests.

```python
# conftest.py
@pytest.fixture
def db():
    database = create_test_db()
    yield database
    database.cleanup()

# test_users.py
def test_creates_user(db):
    user = db.create_user(name="Alice")
    assert user.id is not None
```

## Bug fix workflow

When fixing a bug:
1. Write a test that reproduces the bug (it must FAIL first)
2. Commit the failing test: `git commit -m "test: reproduce bug #123"`
3. Fix the bug
4. The test should now PASS
5. Commit the fix: `git commit -m "fix: resolve bug #123"`

This proves the fix works and prevents regression.

## Coverage targets

- New code: 80% line coverage minimum
- Critical paths (auth, payments, data validation): 95%+
- Check: `pytest --cov=src --cov-report=term-missing`

Don't chase 100% — test behavior, not lines.
