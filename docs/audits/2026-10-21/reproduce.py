"""Read-only baseline probes. Creates isolated temporary packages under .scratch.

Run from any directory: python docs/audits/2026-10-21/reproduce.py
Outputs observations, not a release verdict. This file remains useful after fixes.
"""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location('fievel_audit', ROOT / 'scripts/fievel.py')
f = importlib.util.module_from_spec(spec)
spec.loader.exec_module(f)


def main():
    scratch = ROOT / '.scratch'
    scratch.mkdir(exist_ok=True)
    temp = tempfile.TemporaryDirectory(dir=scratch)
    observations = []
    try:
        folder = f.initialize(Path(temp.name) / 'early-stage')
        path = folder / 'standards.json'
        standards = f.read(path)
        standards['rules'].append({'id':'content-new','instruction':'Use clear next steps.',
                                   'status':'draft','source_ids':[]})
        path.write_text(json.dumps(standards),encoding='utf-8')
        try:
            f.validate(folder)
            value = 'accepted'
        except ValueError as exc:
            value = str(exc)
        observations.append({'finding':'F-01','probe':'Validate a stage-2 draft with one rule and no stage-5 checks','observation':value})

        example = f.initialize(Path(temp.name) / 'example',example=True)
        report = f.review_sheet(example,f.read(ROOT/'examples/responses-good.json'))
        observations.append({'finding':'F-03','probe':'Can a saved review reproduce scenario context and rubric without the current package?',
            'observation':{'has_scenarios':'scenarios' in report,'has_package_snapshot':'system_snapshot' in report,
                           'has_per_check_rubric':all('rubric' in row for row in report['judgments'])}})

        definition = f.read(example/'evaluation.json')
        for scenario in definition['scenarios']:
            for check in scenario['checks']:
                check.update(method='human',value='')
        (example/'evaluation.json').write_text(json.dumps(definition),encoding='utf-8')
        report = f.evaluate(example,{'payment-unknown':'I do not know.'})
        observations.append({'finding':'F-04','probe':'Run a human-only definition against one supplied response',
                             'observation':{'kind':report['kind'],'summary':report['summary']}})

        adapters_root = Path(temp.name)/'adapter-probe'
        for folder_name in ('.agents/skills','.claude/skills'):
            shutil.copytree(ROOT/folder_name,adapters_root/folder_name)
        for filename in ('CLAUDE.md','.github/copilot-instructions.md'):
            target=adapters_root/filename
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(ROOT/filename,target)
        orphan=adapters_root/'.claude/skills/retired-probe/SKILL.md'
        orphan.parent.mkdir()
        orphan.write_text('---\nname: retired-probe\ndescription: Audit fixture\n---\n',encoding='utf-8')
        original_root=f.ROOT
        try:
            f.ROOT=adapters_root
            value=f.adapters(check=True)
            observations.append({'finding':'F-05','probe':'Check adapters with an extra stale Claude skill',
                                 'observation':{'check_passed':True,'expected_adapters':value,'extra_skill_present':orphan.exists()}})
        finally:
            f.ROOT=original_root
        print(json.dumps({'scope':'isolated executable probes, not learner or live-agent tests','observations':observations},indent=2))
    finally:
        assert Path(temp.name).resolve().is_relative_to(scratch.resolve())
        temp.cleanup()


if __name__=='__main__':
    main()
