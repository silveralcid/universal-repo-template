"""Advisory context-size guardrails, with optional failing CI threshold."""
from __future__ import annotations
from pathlib import Path
from .core import safe_path, load_json, text, markdown_files
from .knowledge import context


def budget_report(root: Path) -> dict:
    cfg = load_json(safe_path(root, '.repo/context-budgets.json'))
    max_file = cfg['max_document_tokens']
    max_guide = cfg['max_area_guide_tokens']
    largest = []
    warnings = []
    for p in markdown_files(root):
        rel = p.relative_to(root).as_posix()
        estimate = (len(text(p)) + 3) // 4
        largest.append((estimate, rel))
        # README is the intentionally comprehensive human reference, not a required agent preload.
        if rel == 'README.md' or rel.startswith('docs/evidence/') or rel.startswith('docs/archive/'):
            continue
        cap = cfg['entrypoints'].get(rel, max_guide if rel.startswith('docs/agents/areas/') else max_file)
        if estimate > cap:
            warnings.append(dict(kind='file', path=rel, estimated_tokens=estimate, limit_tokens=cap,
                                 advice='Split by coherent area or section, keep canonical owner and links.'))
    topics = load_json(safe_path(root, 'docs/context/routes.json'))['topics']
    route_reports = []
    for topic in topics:
        pack = context(root, topic)
        estimate = pack['estimated_tokens']
        limit = pack['budget_tokens']
        route_reports.append(dict(topic=topic, required_estimated_tokens=estimate, limit_tokens=limit))
        if limit is not None and estimate > limit:
            warnings.append(dict(kind='route', path=topic, estimated_tokens=estimate, limit_tokens=limit,
                                 advice='Trim required sources or increase budget with a documented reason.'))
    return dict(estimate_method='characters / 4; NOT exact provider tokenization or billed usage',
                status='OVER_BUDGET' if warnings else 'WITHIN_CONFIGURED_LIMITS',
                warnings=warnings, route_budgets=route_reports,
                largest=sorted(largest, reverse=True)[:15],
                total_estimated_tokens=sum(size for size, _ in largest),
                note='Documentation inventory, not session usage. README and historical evidence intentionally exempt from per-file enforcement.')


def budget_config_errors(root: Path) -> list[str]:
    try:
        c = load_json(safe_path(root, '.repo/context-budgets.json'))
    except (ValueError, OSError):
        return ['Invalid or missing context budget configuration']
    errs = []
    if not isinstance(c, dict) or c.get('schema_version') != 1:
        return ['Context budget schema must be 1']
    for key in ('max_document_tokens', 'max_area_guide_tokens'):
        v = c.get(key)
        if type(v) is not int or not 100 <= v <= 100000:
            errs.append(f'{key} must be an integer between 100 and 100000')
    if not isinstance(c.get('entrypoints'), dict):
        errs.append('entrypoints must be a path-to-integer mapping')
    else:
        for rel, limit in c['entrypoints'].items():
            try:
                safe_path(root, rel)
            except ValueError:
                errs.append(f'Invalid entrypoint path: {rel}')
            if type(limit) is not int or not 100 <= limit <= 100000:
                errs.append(f'Invalid entrypoint threshold: {rel}')
    return errs
