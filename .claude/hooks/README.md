# Hooks extension point (inactive)

This folder contains **no runnable hooks** and `.claude/settings.json` enables none. Hook execution is an external side effect that can degrade startup performance or change files, so configure it only with a documented use case, timeout, permission review, portability check and rollback. Do not install a hook that duplicates `AGENTS.md` or automatically dumps large documentation into the context window.
