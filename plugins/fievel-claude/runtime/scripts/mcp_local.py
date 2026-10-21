"""Fievel's local MCP server: structured tools over the Fievel CLI, run on the user's computer.

Speaks MCP over stdio (newline-delimited JSON-RPC). Every path is resolved inside the
workspace (FIEVEL_WORKSPACE, else the current directory); outputs are always new files.
No network access and no model calls.
"""
import json
import os
from pathlib import Path
import platform
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.mcp_protocol import Server, Tool  # noqa: E402
from scripts.mcp_tools import VERSION, knowledge_tools  # noqa: E402

WORKSPACE = Path(os.environ.get('FIEVEL_WORKSPACE') or os.getcwd()).resolve()
SETUP = ('The jsonschema package is missing. With the user\'s permission, create .fievel-venv in the '
         'workspace and install the plugin\'s runtime/requirements.txt with it, then call this tool again.')


def _use_workspace_environment():
    """Let a server started with the system Python find jsonschema in the workspace's .fievel-venv."""
    venv = WORKSPACE / '.fievel-venv'
    for site in [venv / 'Lib' / 'site-packages', *sorted(venv.glob('lib/python3*/site-packages'))]:
        if site.is_dir() and str(site) not in sys.path:
            sys.path.append(str(site))


def core():
    _use_workspace_environment()
    try:
        from scripts import fievel
    except SystemExit:  # fievel.py exits when jsonschema cannot be imported.
        raise ValueError(SETUP) from None
    return fievel


def inside(path, must_exist=False):
    """Resolve a path within the workspace; reject anything that escapes it."""
    if not isinstance(path, str) or not path.strip():
        raise ValueError('Provide a path inside the workspace.')
    resolved = (WORKSPACE / path).resolve()
    if not resolved.is_relative_to(WORKSPACE):
        raise ValueError(f'Path is outside the workspace ({WORKSPACE}): {path}')
    if must_exist and not resolved.exists():
        raise FileNotFoundError(f'Not found in the workspace: {path}')
    return resolved


def optional(path):
    return inside(path, must_exist=True) if path else None


def setup_status():
    try:
        core()
        ready = True
    except ValueError:
        ready = False
    return {'ready': ready, 'python': platform.python_version(), 'workspace': str(WORKSPACE),
            'runtime': str(ROOT), 'next_step': None if ready else SETUP}


def init(folder, example=False):
    target = core().initialize(inside(folder), example)
    return {'created': str(target), 'example': example,
            'note': 'Draft templates only; nothing is approved. Save progress after each meaningful step.'}


def validate(folder, require_coverage=False):
    f = core()
    data = f.validate(inside(folder, must_exist=True), require_coverage=require_coverage)
    return {'valid': True, 'uncovered_rules': f.coverage_gaps(data),
            'note': 'Structure and links are valid. This is not content approval.'}


def status(folder):
    f = core()
    data = f.validate(inside(folder, must_exist=True))
    progress = data['progress']
    return {'path': progress['path'], 'explanations': progress['explanations'],
            'stages': [{'stage': i, 'name': name, 'status': progress['stages'][str(i)]}
                       for i, name in enumerate(f.STAGES, 1)],
            'decisions': progress.get('decisions', []), 'open_questions': progress.get('open_questions', []),
            'next_action': progress['next_action'], 'uncovered_rules': f.coverage_gaps(data)}


def check(folder, responses_file, out):
    f = core()
    result = f.evaluate(inside(folder, must_exist=True), f.read(inside(responses_file, must_exist=True)))
    f.write_new(inside(out), result)
    failures = [{k: row[k] for k in ('scenario_id', 'check_id', 'requirement_id', 'question')}
                for row in result['results'] if row['status'] == 'fail']
    return {'saved': out, 'summary': result['summary'], 'failures': failures,
            'note': 'not_run includes human questions and situations without saved responses. '
                    'Literal checks are not an overall quality verdict.'}


def review(folder, responses_file, out, evidence_config=''):
    f = core()
    responses = f.read(inside(responses_file, must_exist=True))
    if evidence_config:
        from scripts.review_evidence import prepare_review
        result = prepare_review(inside(folder, must_exist=True), responses, f.read(optional(evidence_config)))
    else:
        result = f.review_sheet(inside(folder, must_exist=True), responses)
    f.write_new(inside(out), result)
    return {'saved': out, 'kind': result['kind'], 'pending': len(result['judgments']),
            'note': 'Every human judgment starts pending. Never fill one in for the reviewer.'}


def view(folder, out, report=''):
    core()
    from scripts.viewer import export_viewer
    path = export_viewer(inside(folder, must_exist=True), inside(out), optional(report))
    return {'saved': str(path), 'note': 'Read-only snapshot. Regenerate to a new filename after edits.'}


def review_page(report, out):
    core()
    from scripts.review_page import export_review_page
    return {'saved': str(export_review_page(inside(report, must_exist=True), inside(out)))}


def validate_review(report, folder='', require_complete=False):
    f = core()
    from scripts.review_evidence import validate_review as run
    counts = run(f.read(inside(report, must_exist=True)), optional(folder), require_complete)
    return {'valid': True, 'counts': counts, 'note': 'A valid record is not content approval.'}


def sources_audit(folder, as_of, provenance='', max_age_days=0):
    f = core()
    from scripts.provenance import audit_sources
    config = f.read(optional(provenance)) if provenance else None
    return audit_sources(inside(folder, must_exist=True), as_of, config, max_age_days or None)


def export_consumer(folder, consumer, as_of, out, include_drafts=False, provenance=''):
    f = core()
    from scripts.consumer import export_consumer as run
    config = f.read(optional(provenance)) if provenance else None
    result = run(inside(folder, must_exist=True), consumer, as_of, include_drafts, config)
    f.write_new(inside(out), result)
    return {'saved': out, 'note': 'Draft review artifact only; no consumer installed, run or evaluated.'}


def text(description):
    return {'type': 'string', 'description': description}


def flag(description):
    return {'type': 'boolean', 'description': description}


FOLDER = text('Project folder inside the workspace, for example my-content-system')
NEW_FILE = text('New output path inside the workspace; existing files are never overwritten')

TOOLS = knowledge_tools() + [
    Tool('fievel_setup_status', 'Check Fievel setup',
         'Report whether Python and the jsonschema dependency are ready, and the workspace Fievel works in.',
         {}, [], setup_status),
    Tool('fievel_init', 'Create a project',
         'Create a NEW Fievel project folder from the empty template, or from the fictional Wayfarer example. '
         'Refuses an existing folder.', {'folder': FOLDER, 'example': flag('Use the fictional practice example')},
         ['folder'], init, read_only=False),
    Tool('fievel_validate', 'Validate a project',
         'Check a project\'s structure and links and list rules that still lack quality checks. '
         'Not content approval.', {'folder': FOLDER, 'require_coverage': flag('Also fail if any rule lacks a check')},
         ['folder'], validate),
    Tool('fievel_status', 'Show project status',
         'Return saved stages, decisions, open questions, next action and uncovered rules for a project.',
         {'folder': FOLDER}, ['folder'], status),
    Tool('fievel_check', 'Check saved responses',
         'Run literal checks against saved responses (JSON mapping situation IDs to response text) and save a new '
         'report. Human questions stay not_run.', {'folder': FOLDER, 'responses_file': text('Saved responses JSON file'),
         'out': NEW_FILE}, ['folder', 'responses_file', 'out'], check, read_only=False),
    Tool('fievel_review', 'Prepare human review',
         'Save a new human review sheet for saved responses, with every judgment pending. With evidence_config, '
         'prepare a self-contained evidence review.', {'folder': FOLDER, 'responses_file': text('Saved responses JSON file'),
         'out': NEW_FILE, 'evidence_config': text('Optional review evidence configuration file')},
         ['folder', 'responses_file', 'out'], review, read_only=False),
    Tool('fievel_view', 'Generate overview',
         'Generate a read-only offline HTML overview of a project, optionally with a selected check report.',
         {'folder': FOLDER, 'out': text('New .html file inside the workspace'),
          'report': text('Optional check report to reproduce')}, ['folder', 'out'], view, read_only=False),
    Tool('fievel_review_page', 'Generate review form',
         'Generate an offline HTML form for completing a saved evidence review.',
         {'report': text('Evidence review JSON file'), 'out': text('New .html file inside the workspace')},
         ['report', 'out'], review_page, read_only=False),
    Tool('fievel_validate_review', 'Validate a review record',
         'Validate a saved evidence review, optionally rejecting it when stale for a project or incomplete.',
         {'report': text('Evidence review JSON file'), 'folder': text('Optional project folder to compare'),
          'require_complete': flag('Fail unless every judgment is complete')}, ['report'], validate_review),
    Tool('fievel_sources_audit', 'Audit source provenance',
         'Audit declared source metadata and optional evidence links. Never opens source locations.',
         {'folder': FOLDER, 'as_of': text('Audit date, YYYY-MM-DD'), 'provenance': text('Optional provenance file'),
          'max_age_days': {'type': 'integer', 'description': 'Optional freshness window the owner supplied'}},
         ['folder', 'as_of'], sources_audit),
    Tool('fievel_export_consumer', 'Export for a consumer',
         'Save a draft review export of selected rules and provenance for a named consuming AI. Installs nothing.',
         {'folder': FOLDER, 'consumer': text('Name of the consuming AI or team'), 'as_of': text('Date, YYYY-MM-DD'),
          'out': NEW_FILE, 'include_drafts': flag('Include draft rules for design review'),
          'provenance': text('Optional provenance file')}, ['folder', 'consumer', 'as_of', 'out'],
         export_consumer, read_only=False),
]

SERVER = Server('fievel-local', VERSION,
                'Fievel tools for a content system in this workspace. Follow the Fievel skills: nothing here '
                'approves content, and human judgments are never filled in by tools.', TOOLS)


def main():
    sys.stdout.reconfigure(encoding='utf-8', newline='\n')
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            message = json.loads(line)
        except ValueError:
            response = {'jsonrpc': '2.0', 'id': None, 'error': {'code': -32700, 'message': 'Parse error'}}
        else:
            response = SERVER.handle(message)
        if response is not None:
            sys.stdout.write(json.dumps(response, ensure_ascii=False) + '\n')
            sys.stdout.flush()


if __name__ == '__main__':
    main()
