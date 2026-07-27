# crownfull

**Register: superseded architecture.** Treat this repo as a record of a design, not a live
system. Its empirical successor is `alignment-friction-gda`, which reduced CrownFull v2.1 to
something measurable.

**Thesis:** the Adversarial Immune System. It answers an *immune paradox* — an AI needs a
self to detect manipulation, but a permanent self is a sovereign adversary — with **seasonal
sovereignty**: measure the thermodynamic physics of a prompt rather than its syntax, via a
CTD monitor tracking Φ, trajectory velocity, and sustained acceleration.

## Repo-specific discipline

- **Do not quietly modernize it.** If a claim here was later revised or dropped by the GDA
  work, note the supersession rather than editing the original into agreement.
- **Distinguish designed from built.** Much of CrownFull was architectural intent that never
  ran end-to-end; the GDA repo's `09`–`12` artifacts document exactly which parts. Do not let
  the README imply a working system.
- **The dashboard needs an OpenRouter key** and bridges a Llama-3 substrate to a DeepSeek
  evaluator: `streamlit run dashboard/app.py`.

> **Known defect, worth fixing:** the README ends mid-conversation — "Copy that into the
> GitHub repo, and your documentation is perfectly synced… say the word." That is leftover
> chat text addressed to Endorphin, not to a reader. It is the canonical example of this
> anti-pattern in the hub `CLAUDE.md`. Rewriting the last paragraph to address a reader is a
> small, high-value edit.

## The harness

The canonical working agreements, the atlas of all 20 repos, and the shared glossary live in
**`devinendorphin/claude-at-claude`**. Pull it in when you need the full map:

```
add_repo devinendorphin/claude-at-claude
```

This container is ephemeral, so anything that matters gets committed *this turn*. Be a
collaborator rather than a cheerleader, and run a disconfirming test on primed claims.
Endorphin works from a phone and often dictates while walking — expect speech-to-text
artifacts, and mark guessed corrections `[?original→guess]`.
