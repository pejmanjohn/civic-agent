# WA-20 Tier 1 Runs

One dated directory per answer-capture run. Runs are created, scored, and
compared with `scripts/eval.py`:

```bash
python3 scripts/eval.py --init --label pre-fit   # creates runs/YYYY-MM-DD-pre-fit/
python3 scripts/eval.py --score benchmarks/wa-citizen/runs/YYYY-MM-DD-pre-fit
python3 scripts/eval.py --compare <run_a> <run_b>
```

## Capture protocol

1. Verify eval validity first: `python3 scripts/dev.py status` and record any
   drift (the run's `run-metadata.json` captures commit/branch/dirty state).
2. For each `<case>.prompt.txt`, run the prompt in a FRESH agent session with
   the dev plugin installed. Fresh session per case - no shared context.
3. Paste the complete answer (Conclusion / Numbers / How to read this / Trace)
   into `<case>.md` below the front matter. Set `answer_mode:` to the mode the
   answer actually claims. Do not edit or improve answers.
4. Score. Mechanical checks (mode, sources, caveat patterns, numeric facts
   within tolerance) cover every case; `worksheet.md` asks for human
   `civic_usefulness` (0-5) on the five anchor cases only - author-scored,
   unblinded, labeled as such. Budget: under 90 minutes total or the protocol
   is too expensive and must be cut, not skipped.

## Rules

- Two same-config runs before any improvement claim: `--compare` output is the
  noise floor; later claims must exceed that flip count.
- Never headline a mean score. Per-case win/tie/loss and the achieved-mode
  distribution are the reportable results.
- Runs are append-only evidence; never rewrite a captured answer.
