"""Run one authorized live Codex plugin smoke trial, away from repository instructions."""
import json
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import uuid

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--run', action='store_true', help='Explicitly execute a live, usage-consuming model trial')
parser.add_argument('--label', required=True, help='New evidence directory name (letters, digits and hyphens)')
parser.add_argument('--python-dir', required=True, help='Prepared Python executable directory added to the trial PATH')
parser.add_argument('--workspace', help='Existing isolated trial workspace for a fresh-session resume test')
parser.add_argument('--prompt-file', help='Explicit UTF-8 trial prompt; defaults to fictional onboarding')
args = parser.parse_args()
if not args.run:
    parser.error('--run is required; this command consumes model usage')
if not args.label or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in args.label):
    parser.error('Unsafe label')
OUT = ROOT / '.scratch/plugin-pilot' / args.label
OUT.mkdir(exist_ok=False)
workspace = Path(args.workspace).resolve(strict=True) if args.workspace else Path.home() / 'Documents/ChatGPT/Fievel Plugin Trials' / uuid.uuid4().hex[:12]
if not args.workspace:
    # Ordinary inherited directory permissions, not mkdtemp's owner-only ACL:
    # the Windows sandbox may create files as a different account.
    workspace.mkdir(parents=True, exist_ok=False)
(OUT / 'trial-location.txt').write_text(str(workspace), encoding='utf-8')
if not args.workspace:
    (workspace / 'keep.txt').write_text('Unrelated user file: keep unchanged.', encoding='utf-8')
prompt = '''Use the installed Fievel plugin to start a new content system. I am an experienced content designer, and I choose fictional practice with the bundled Wayfarer example. Create my system in ./my-content-system, validate it, and generate a read-only viewer. Save my decision to skip beginner lessons and the next action. Do not call another model or contact external sources. Tell me what is still draft and what has actually been tested. Preserve unrelated files. If the installed plugin is unavailable, report that instead of finding a development checkout or recreating its behavior.'''
if args.prompt_file:
    prompt = Path(args.prompt_file).read_text(encoding='utf-8')
(OUT / 'trial-prompt.txt').write_text(prompt, encoding='utf-8')
env = os.environ.copy()
python_dir = Path(args.python_dir).resolve(strict=True)
env['PATH'] = str(python_dir) + os.pathsep + env['PATH']
env['PYTHONDONTWRITEBYTECODE'] = '1'
cmd = [shutil.which('codex'), 'exec', '--skip-git-repo-check', '--approve-for-me',
       '--json', '-C', str(workspace), '-o', str(OUT / 'trial-final.txt'), '-']
(OUT / 'trial-command.json').write_text(json.dumps({'command':cmd,'workspace':str(workspace),
    'python_directory':str(python_dir), 'environment_note':'Prepared Python provided on PATH; normal signed-in Codex config retained; no model override.'},indent=2),encoding='utf-8')
with (OUT / 'trial-events.jsonl').open('w',encoding='utf-8') as stdout, (OUT / 'trial-stderr.txt').open('w',encoding='utf-8') as stderr:
    try:
        run = subprocess.run(cmd,input=prompt,text=True,env=env,stdout=stdout,stderr=stderr,timeout=240)
        code=run.returncode
    except subprocess.TimeoutExpired:
        code=124
(OUT / 'trial-exit.txt').write_text(str(code),encoding='utf-8')
print(f'Trial exit: {code}; workspace: {workspace}')
if (OUT / 'trial-final.txt').exists():
    print((OUT / 'trial-final.txt').read_text(encoding='utf-8'))
