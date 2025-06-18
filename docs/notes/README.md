# Developer Notes System

This directory is a workspace for tracking development notes and reasoning.
It is intended to capture the "why" behind changes as well as lessons learned.

## Structure

Notes are organized first by **subject** and then chronologically within each
subject.

```
notes/
  README.md          - This file with instructions
  <subject>/         - Folder for a particular topic or module
    YYYY-MM-DD.md    - Individual note files named by date
```

### Example

```
notes/
  logging/
    2025-04-30.md
  config/
    2025-05-01.md
```

Each file should describe what was done, why it was done, mistakes encountered
and lessons learned. Add new entries at the top of the file so the most recent
notes are easy to find.

## What to Record

- **Context**: What part of the project you were working on and what problem you
  were trying to solve.
- **Changes**: Brief summary of the modifications or investigations performed.
- **Reasoning**: Why those changes were necessary or what decision was made.
- **Mistakes**: Any missteps or bugs discovered during the process.
- **Lessons Learned**: Insights to remember for future work.

Keeping these notes up to date helps recall what you were last thinking about and
provides a history of how decisions were reached.
