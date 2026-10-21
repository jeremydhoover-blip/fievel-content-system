"""Tools shared by Fievel's local and remote MCP servers: the bundled knowledge library,
package templates and the package format. Read-only; never touches user files."""
import json
from pathlib import Path

from scripts.mcp_protocol import Tool

ROOT = Path(__file__).resolve().parents[1]
FILES = ('product', 'standards', 'sources', 'behavior', 'evaluation', 'governance', 'progress')
VERSION = (ROOT / 'VERSION').read_text(encoding='utf-8').strip()


def list_lessons():
    lessons = [p.relative_to(ROOT / 'knowledge').as_posix() for p in sorted((ROOT / 'knowledge').rglob('*.md'))
               if p.name != 'INDEX.md']
    return {'index': (ROOT / 'knowledge/INDEX.md').read_text(encoding='utf-8'), 'lessons': lessons,
            'note': 'Educational guidance, not organizational policy.'}


def get_lesson(path):
    allowed = set(list_lessons()['lessons'])
    if path not in allowed:
        raise ValueError('Unknown lesson. Use fievel_list_lessons for valid paths.')
    return {'path': path, 'text': (ROOT / 'knowledge' / path).read_text(encoding='utf-8')}


def read_package(folder):
    return {name: json.loads((folder / f'{name}.json').read_text(encoding='utf-8')) for name in FILES}


def get_template(example=False):
    folder = ROOT / ('examples/wayfarer' if example else 'templates/content-system')
    return {'kind': 'fictional_example' if example else 'empty_template', 'files': {
        f'{name}.json': value for name, value in read_package(folder).items()},
        'note': 'Save each file in a NEW project folder. Templates keep unknowns explicit; '
                'the example is fictional training material, not policy.'}


def get_schema():
    return {'schema': json.loads((ROOT / 'schemas/content-system.schema.json').read_text(encoding='utf-8')),
            'files': [f'{name}.json' for name in FILES]}


def knowledge_tools():
    return [
        Tool('fievel_list_lessons', 'List Fievel lessons',
             'List the bundled Fievel knowledge modules and the index that says which to read at each stage. '
             'Educational guidance, not organizational policy.', {}, [], list_lessons),
        Tool('fievel_get_lesson', 'Read a Fievel lesson',
             'Read one bundled Fievel knowledge module by the path fievel_list_lessons returns.',
             {'path': {'type': 'string', 'description': 'Lesson path, for example content-design/content-systems.md'}},
             ['path'], get_lesson),
        Tool('fievel_get_template', 'Get project template',
             'Return the seven files of an empty Fievel content-system template, or of the fictional '
             'Wayfarer example when example is true.',
             {'example': {'type': 'boolean', 'description': 'Return the fictional example instead of the empty template'}},
             [], get_template),
        Tool('fievel_get_schema', 'Get package format',
             'Return the JSON Schema that every Fievel package must satisfy and the seven file names.',
             {}, [], get_schema),
    ]
