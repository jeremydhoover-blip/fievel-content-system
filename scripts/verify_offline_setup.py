"""Reproduce offline setup checks using a new local workspace and venv.

No network or model calls. Local dependency copying is reported separately from
installation. Existing output directories are refused and scratch files retained.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import venv

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',required=True,help='New evidence directory inside this repository')
    args=parser.parse_args()
    out=Path(args.out).resolve()
    if not out.is_relative_to(ROOT) or out.exists():
        raise SystemExit('Choose a new evidence directory inside the repository')
    out.mkdir(parents=True)
    scratch=ROOT/'.scratch'
    scratch.mkdir(exist_ok=True)
    import tempfile
    work=Path(tempfile.mkdtemp(prefix='offline-setup-',dir=scratch))
    workspace=work/'workspace'
    workspace.mkdir()
    for name in ('scripts','schemas','templates','examples','viewer','review-ui','knowledge','tests','.agents','.claude'):
        shutil.copytree(ROOT/name,workspace/name,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    for name in ('AGENTS.md','CLAUDE.md','README.md','requirements.txt','VERSION'):
        shutil.copyfile(ROOT/name,workspace/name)
    (workspace/'.github').mkdir()
    shutil.copyfile(ROOT/'.github/copilot-instructions.md',workspace/'.github/copilot-instructions.md')
    local_temp=work/'temp'
    local_temp.mkdir()
    tempfile.tempdir=str(local_temp)
    os.environ['TMP']=str(local_temp)
    os.environ['TEMP']=str(local_temp)
    envdir=work/'venv'
    try:
        venv.create(envdir,with_pip=True,system_site_packages=False)
    except (OSError, subprocess.CalledProcessError) as exc:
        output=getattr(exc,'output',b'')
        if isinstance(output,bytes):output=output.decode('utf-8',errors='replace')
        (out/'setup-failure.json').write_text(json.dumps({'stage':'venv_bootstrap','error':str(exc),'output':output,'workspace':str(workspace)},indent=2),encoding='utf-8')
        raise SystemExit(f'Local venv bootstrap failed; see {out}/setup-failure.json')
    python=envdir/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
    env=os.environ.copy()
    env.pop('PYTHONPATH',None)
    env.pop('PYTHONHOME',None)
    env.update(PIP_CONFIG_FILE=os.devnull,PIP_DISABLE_PIP_VERSION_CHECK='1',PIP_NO_INDEX='1')
    records=[]
    def run(label,arguments,cwd=workspace,expect=0):
        command=[str(python),'-I',*map(str,arguments)]
        result=subprocess.run(command,cwd=cwd,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace')
        records.append(dict(label=label,command=command,exit_code=result.returncode,
                            expected_exit=expect,stdout=result.stdout,stderr=result.stderr))
        (out/'steps.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
        return result
    run('runtime',['-c','import sys,site; print(sys.version); print(sys.prefix); print(site.ENABLE_USER_SITE)'])
    missing=run('missing_dependency',['scripts/fievel.py','validate','templates/content-system'],expect=1)
    install=run('offline_install',['-m','pip','install','--no-index','--no-cache-dir','--target','.deps','-r','requirements.txt'],expect=None)
    if install.returncode:
        # Copying an installed runtime is not represented as a successful pip install.
        shutil.copytree(ROOT/'.deps',workspace/'.deps',dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    run('dependency_versions',['-c',"import sys,importlib.metadata as m; sys.path.insert(0,'.deps'); print({n:m.version(n) for n in ['jsonschema','attrs','jsonschema-specifications','referencing','rpds-py','typing-extensions']})"])
    cli=[str(workspace/'scripts/fievel.py')]
    project=workspace/'my-content-system'
    run('initialize',cli+['init',project,'--example'])
    run('validate',cli+['validate',project,'--require-coverage'])
    run('status',cli+['status',project])
    run('check',cli+['check',project,'--responses',workspace/'examples/responses-good.json','--out',project/'results/check.json'])
    run('pending_review',cli+['review',project,'--responses',workspace/'examples/responses-good.json','--evidence-config',workspace/'examples/review-evidence-config.json','--out',project/'results/review.json'])
    run('validate_pending',cli+['validate-review',project/'results/review.json'])
    run('reject_incomplete',cli+['validate-review',project/'results/review.json','--require-complete'],expect=2)
    run('source_audit',cli+['sources-audit',project,'--as-of','2026-10-21','--provenance',workspace/'examples/source-provenance.json','--max-age-days','365','--strict'])
    run('consumer_export',cli+['export-consumer',project,'--consumer','Offline fictional fixture','--as-of','2026-10-21','--include-drafts','--out',project/'results/consumer.json'])
    run('viewer',cli+['view',project,'--report',project/'results/check.json','--out',project/'results/overview.html'])
    run('overwrite_refusal',cli+['check',project,'--responses',workspace/'examples/responses-good.json','--out',project/'results/check.json'],expect=2)
    run('adapter_integrity',cli+['sync','--check'])
    run('full_tests',['-m','unittest','discover','-s','tests','-v'])
    failures=[r['label'] for r in records if r['expected_exit'] is not None and r['exit_code']!=r['expected_exit']]
    summary={'kind':'offline_setup_evidence','platform':platform.platform(),'python':platform.python_version(),
             'workspace':str(workspace),'venv':str(envdir),'model_calls':0,'downloads_attempted':False,
             'pip_install_succeeded':install.returncode==0,'runtime_recovery':'not_needed' if install.returncode==0 else 'copied_existing_local_dependencies',
             'unexpected_failures':failures,'missing_dependency_message_verified':'Install the validator first' in missing.stderr,
             'limitations':['Single Windows/Python environment only','Installed dependency copying is not clean pip installation','No agent host activation or model behavior tested']}
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    hashes={p.relative_to(ROOT/'.deps').as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'.deps').rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    (out/'local-dependency-hashes.json').write_text(json.dumps(hashes,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))
    return 1 if failures else 0


if __name__=='__main__':
    sys.exit(main())
