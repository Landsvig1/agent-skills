---
name: wrap
description: >
  Wrap up the current session: check whether work is actually finished, then
  give a concise report of what was done. Make sure to use this whenever the
  user signals they're ending the session or moving on — "wrap up", "wrap
  this up", "/wrap", "let's stop here", "that's it for today", "I'm done
  here", "let's call it", "good for now", "one more thing then I'm out", or
  similar, even if they don't use the word "wrap" explicitly.
---

# Wrap up

1. Ask yourself two questions before writing the report:
   - Is there anything I said I'd do in this session that isn't actually done
     (unfinished edits, a promised follow-up, a failing test, an unanswered
     question)?
   - Is there anything left in a broken or half-changed state (uncommitted
     changes that should be committed, a file left mid-edit, a todo left
     incomplete)?

2. If either answer surfaces unfinished work, only finish it now if it's
   small and safe (e.g. closing out a trivial edit). Anything risky or
   hard-to-reverse — committing, pushing, deleting, sending — is not yours
   to do just because the session is ending; name it plainly as open and let
   the user decide. Don't report completion prematurely either way.

3. Once clear, write a short report for the user:
   - 3-6 bullet points max, what was actually done this session
   - One line on anything left open, or "nothing outstanding" if clean
   - No filler, no restating the request, no next-steps essay
