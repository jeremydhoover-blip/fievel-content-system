"""Fievel's remote MCP server: stateless tools over package content the agent sends.

Serves MCP Streamable HTTP at POST /mcp with JSON responses. Nothing sent is stored or
logged: requests are processed in memory and discarded. No accounts, no model calls.
Configure with PORT, and optionally FIEVEL_CHALLENGE_PATH and FIEVEL_CHALLENGE_TOKEN for
the directory's domain-verification challenge.
"""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import fievel as f  # noqa: E402
from scripts.mcp_protocol import INVALID_REQUEST, PARSE_ERROR, Server, Tool  # noqa: E402
from scripts.mcp_tools import VERSION, knowledge_tools  # noqa: E402

MAX_BODY = 2 * 1024 * 1024


def package_data(package):
    if not isinstance(package, dict) or set(package) != set(f.FILES):
        raise ValueError('package must be an object with exactly these keys: ' + ', '.join(f.FILES)
                         + ' (the parsed contents of each .json file).')
    return json.loads(json.dumps(package))  # Detached copy; validation never mutates input.


def validate_package(package, require_coverage=False):
    data = f.validate_data(package_data(package), require_coverage)
    return {'valid': True, 'uncovered_rules': f.coverage_gaps(data), 'system_scope': f.SYSTEM_SCOPE,
            'system_sha256': f.system_fingerprint(data),
            'note': 'Structure and links are valid. This is not content approval. Nothing was stored.'}


def check_responses(package, responses):
    data = f.validate_data(package_data(package), require_coverage=True)
    report = f.evaluate_data(data, responses)
    return {'report': report, 'note': 'Save report as a NEW file in the project results folder. '
            'Human questions stay not_run; literal checks are not an overall quality verdict. Nothing was stored.'}


PACKAGE = {'type': 'object', 'description': 'The seven Fievel files, keyed product, standards, sources, behavior, '
           'evaluation, governance, progress, each holding that file\'s parsed JSON'}

TOOLS = knowledge_tools() + [
    Tool('fievel_validate_package', 'Validate a package',
         'Check a Fievel package\'s structure and links and list rules that still lack quality checks. '
         'Stateless: the package is not stored. Not content approval.',
         {'package': PACKAGE, 'require_coverage': {'type': 'boolean', 'description': 'Also fail if any rule lacks a check'}},
         ['package'], validate_package),
    Tool('fievel_check_responses', 'Check saved responses',
         'Run literal checks for a fully covered package against saved responses (situation ID to response text) and '
         'return a report to save. Human questions stay not_run. Stateless: nothing is stored.',
         {'package': PACKAGE, 'responses': {'type': 'object', 'description': 'Situation IDs mapped to saved response text'}},
         ['package', 'responses'], check_responses),
]

SERVER = Server('fievel-remote', VERSION,
                'Stateless Fievel tools: lessons, templates, the package format, validation and literal checks. '
                'Follow the Fievel skills. Nothing sent here is stored; nothing here approves content.', TOOLS)


class Handler(BaseHTTPRequestHandler):
    server_version = 'fievel-mcp'
    sys_version = ''

    def log_message(self, format, *args):
        # Never log request bodies or query strings: content stays private.
        sys.stderr.write(f'{self.command} {self.path.split("?")[0]} {args[1] if len(args) > 1 else ""}\n')

    def send(self, status, body=b'', content_type='application/json', headers=()):
        self.send_response(status)
        if body:
            self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        for key, value in headers:
            self.send_header(key, value)
        self.end_headers()
        if body and self.command != 'HEAD':
            self.wfile.write(body)

    def send_json(self, status, value):
        self.send(status, json.dumps(value, ensure_ascii=False).encode('utf-8'))

    def do_GET(self):
        path = self.path.split('?')[0]
        challenge_path, token = os.environ.get('FIEVEL_CHALLENGE_PATH'), os.environ.get('FIEVEL_CHALLENGE_TOKEN')
        if challenge_path and token and path == challenge_path:
            self.send(200, token.encode('utf-8'), 'text/plain; charset=utf-8')
        elif path == '/mcp':
            self.send(405, headers=[('Allow', 'POST')])
        elif path in ('/', '/healthz'):
            self.send_json(200, {'name': 'fievel-remote', 'version': VERSION, 'mcp': '/mcp',
                                 'privacy': 'https://jeremydhoover-blip.github.io/fievel-content-system/privacy.html'})
        else:
            self.send_json(404, {'error': 'Not found'})

    do_HEAD = do_GET

    def do_DELETE(self):
        self.send(405, headers=[('Allow', 'POST')])

    def do_POST(self):
        if self.path.split('?')[0] != '/mcp':
            return self.send_json(404, {'error': 'Not found'})
        try:
            length = int(self.headers.get('Content-Length', ''))
        except ValueError:
            return self.send_json(411, {'error': 'Content-Length required'})
        if length > MAX_BODY:
            return self.send_json(413, {'error': f'Request larger than {MAX_BODY} bytes'})
        try:
            message = f.decode_json(self.rfile.read(length), 'request')
        except ValueError:
            return self.send_json(400, {'jsonrpc': '2.0', 'id': None, 'error': {'code': PARSE_ERROR, 'message': 'Parse error'}})
        if isinstance(message, list):
            return self.send_json(400, {'jsonrpc': '2.0', 'id': None,
                                        'error': {'code': INVALID_REQUEST, 'message': 'Batch requests are not supported'}})
        response = SERVER.handle(message)
        if response is None:
            return self.send(202)
        self.send_json(200, response)


def main():
    port = int(os.environ.get('PORT', '8080'))
    ThreadingHTTPServer(('0.0.0.0', port), Handler).serve_forever()


if __name__ == '__main__':
    main()
