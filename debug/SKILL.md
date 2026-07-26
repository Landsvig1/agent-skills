---
name: debug
description: >
  Systematic debugging process: reproduce, isolate, hypothesize, verify.
  Trigger when: a test fails unexpectedly; when code produces wrong output;
  when an exception is thrown; when stuck after 2 attempts at fixing something.
  Do NOT trigger for design questions or review tasks.
---

# Systematic Debugging

Debugging is science: form a hypothesis, design an experiment, check the result.

## Quick start

```bash
# Step 1: Reproduce it
# Run the exact failing command. Copy the FULL error output.

# Step 2: Read the traceback bottom-up (the innermost frame is usually the real error)

# Step 3: Form ONE hypothesis about the cause

# Step 4: Add a targeted print/log to test the hypothesis
# DO NOT add 10 print statements — one precise one

# Step 5: Run again. Confirmed or denied? Adjust hypothesis.
```

## The process

### 1. Reproduce (mandatory)
If you can't reproduce it, you can't debug it.

```bash
# Reproduce with the minimal possible command
python -m pytest tests/test_auth.py::test_login_fails -xvs 2>&1 | head -50
```

`-x`: stop at first failure
`-v`: verbose output
`-s`: show print output
`2>&1`: capture stderr too

### 2. Read the error

A Python traceback reads bottom-up. The last frame is where the error occurred.

```
Traceback (most recent call last):
  File "tests/test_auth.py", line 23, in test_login_fails    ← test file
    result = auth.login("alice", "wrong_password")
  File "src/auth.py", line 47, in login                       ← your code
    return self._db.get_user(username)
  File "src/db.py", line 112, in get_user                     ← the actual error
    raise ConnectionError("DB connection refused")
ConnectionError: DB connection refused                         ← read this first
```

The error is `ConnectionError` in `db.py:112`. Start there, not in `test_auth.py`.

### 3. Hypothesize

Good hypothesis: specific and falsifiable.
- ✅ "The DB fixture isn't starting before the test runs"
- ❌ "Something is wrong with the database"

### 4. Minimum diagnostic

Add ONE targeted observation:

```python
# To test: "is the DB fixture starting?"
def get_user(self, username):
    print(f"DB connection URL: {self.url}")  # ← one line
    print(f"DB connected: {self.connection is not None}")
    raise ConnectionError("DB connection refused")
```

Run, observe, update hypothesis.

### 5. Binary search for the source

If the error location isn't obvious:

```python
# Add a checkpoint to narrow the range
def process(data):
    print("checkpoint 1: starting")  # does this print?
    result = transform(data)
    print("checkpoint 2: transform done")  # does this print?
    return validate(result)
```

Bisect until you find the line that doesn't execute when you expect it to.

## Common patterns

### "It works locally but fails in CI"
- Environment variable missing: check `os.environ` output
- Database not seeded: check test fixtures
- Race condition: add explicit wait or make test synchronous

### "It was working, now it's not"
```bash
git bisect start
git bisect bad HEAD
git bisect good {last-known-good-commit}
# git bisect run pytest tests/test_broken.py
```

### "The test passes but the behavior is wrong"
The test is testing the wrong thing. Find what the test should assert and add that assertion.

### "I don't know where to start"

```bash
# Find all places the error message is generated
grep -rn "ConnectionError\|connection refused" src/

# Find all callers of the failing function
grep -rn "get_user(" src/ tests/
```

## Debug output format

When stuck, structure your findings like this:

```markdown
## Debug report: {what's broken}

### Error
```
{exact error message and traceback}
```

### Hypotheses tried
1. {Hypothesis 1} → {Result: confirmed/denied} → {What this tells us}
2. {Hypothesis 2} → {Result: ...}

### Current best hypothesis
{Specific, with evidence}

### Next experiments
- {What to try next}
- {What information is needed}

### Blocker
{If stuck: what human decision or information is needed}
```
