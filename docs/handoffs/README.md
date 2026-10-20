# Work handoffs

Track high-value continuation packets in [`active/`](active/) and finished or obsolete packets in [`completed/`](completed/). A handoff is a snapshot of context, **not an authoritative live branch/PR registry**. Before resuming, recheck Git and project decisions. For single-message or trivial changes, no handoff file is necessary.

New blank packet: `python tools/repo.py new handoff --slug <task> --bucket active`. See [continuation guide](../agents/handoff.md) and [research/evidence policy](../agents/research-and-evidence.md).
