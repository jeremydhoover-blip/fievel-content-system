"""Fievel's local (stdio) and remote (HTTP) MCP servers."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

from scripts import mcp_remote
from scripts.mcp_protocol import Server, Tool

ROOT = Path(__file__).resolve().parents[1]
FILES = ('product', 'standards', 'sources', 'behavior', 'evaluation', 'governance', 'progress')
PACKAGE = {n: json.loads((ROOT / f'examples/wayfarer/{n}.json').read_text(encoding='utf-8')) for n in FILES}
BAD = json.loads((ROOT / 'examples/responses-bad.json').read_text(encoding='utf-8'))


def call(request_id, name, arguments):
    return {'jsonrpc': '2.0', 'id': request_id, 'method': 'tools/call', 'params': {'name': name, 'arguments': arguments}}


class ProtocolTests(unittest.TestCase):
    def setUp(self):
        self.server = Server('t', '1', 'test', [Tool('echo', 'Echo', 'Echo', {'text': {'type': 'string'}}, ['text'],
                                                     lambda text: {'text': text})])

    def test_messages(self):
        init = self.server.handle({'jsonrpc': '2.0', 'id': 1, 'method': 'initialize',
                                   'params': {'protocolVersion': '2025-03-26'}})
        self.assertEqual(init['result']['protocolVersion'], '2025-03-26')
        future = self.server.handle({'jsonrpc': '2.0', 'id': 2, 'method': 'initialize', 'params': {'protocolVersion': '2099-01-01'}})
        self.assertEqual(future['result']['protocolVersion'], '2025-06-18')
        self.assertIsNone(self.server.handle({'jsonrpc': '2.0', 'method': 'notifications/initialized'}))
        self.assertEqual(self.server.handle({'jsonrpc': '2.0', 'id': 3, 'method': 'nope'})['error']['code'], -32601)
        self.assertEqual(self.server.handle(call(4, 'echo', {'text': 'hi'}))['result']['structuredContent'], {'text': 'hi'})
        for arguments in ({}, {'text': 1}, {'text': 'x', 'extra': 1}):
            self.assertTrue(self.server.handle(call(5, 'echo', arguments))['result']['isError'], arguments)
        self.assertEqual(self.server.handle(call(6, 'missing', {}))['error']['code'], -32602)
        self.assertEqual(self.server.handle({'id': 7})['error']['code'], -32600)


class LocalServerTests(unittest.TestCase):
    def run_server(self, messages, workspace):
        env = dict(os.environ, FIEVEL_WORKSPACE=str(workspace), PYTHONPATH=str(ROOT / '.deps'), PYTHONDONTWRITEBYTECODE='1')
        proc = subprocess.run([sys.executable, str(ROOT / 'scripts/mcp_local.py')], input=''.join(json.dumps(m) + '\n' for m in messages),
                              capture_output=True, text=True, encoding='utf-8', env=env, cwd=str(ROOT))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return {r['id']: r for r in map(json.loads, proc.stdout.splitlines())}

    def test_workflow_and_workspace_boundary(self):
        scratch = ROOT / '.scratch'
        scratch.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as tmp:
            workspace = Path(tmp)
            (workspace / 'responses.json').write_text(json.dumps(BAD), encoding='utf-8')
            replies = self.run_server([
                {'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {'protocolVersion': '2025-06-18'}},
                {'jsonrpc': '2.0', 'method': 'notifications/initialized'},
                {'jsonrpc': '2.0', 'id': 2, 'method': 'tools/list'},
                call(3, 'fievel_init', {'folder': 'system', 'example': True}),
                call(4, 'fievel_validate', {'folder': 'system', 'require_coverage': True}),
                call(5, 'fievel_check', {'folder': 'system', 'responses_file': 'responses.json', 'out': 'results/run-01.json'}),
                call(6, 'fievel_check', {'folder': 'system', 'responses_file': 'responses.json', 'out': 'results/run-01.json'}),
                call(7, 'fievel_review', {'folder': 'system', 'responses_file': 'responses.json', 'out': 'results/review-01.json'}),
                call(8, 'fievel_status', {'folder': 'system'}),
                call(9, 'fievel_view', {'folder': 'system', 'out': 'overview.html', 'report': 'results/run-01.json'}),
                call(10, 'fievel_init', {'folder': '../escape'}),
                call(11, 'fievel_validate', {'folder': str(ROOT / 'examples/wayfarer')}),
                call(12, 'fievel_get_lesson', {'path': '../AGENTS.md'}),
                call(13, 'fievel_get_lesson', {'path': 'content-design/content-systems.md'}),
            ], workspace)
            self.assertEqual(replies[1]['result']['serverInfo']['name'], 'fievel-local')
            names = {t['name'] for t in replies[2]['result']['tools']}
            self.assertTrue({'fievel_init', 'fievel_check', 'fievel_view', 'fievel_get_lesson'} <= names)
            for i in (3, 4, 5, 7, 8, 9, 13):
                self.assertFalse(replies[i]['result']['isError'], replies[i])
            self.assertEqual(replies[5]['result']['structuredContent']['summary'], {'pass': 0, 'fail': 3, 'not_run': 6})
            self.assertEqual(replies[7]['result']['structuredContent']['pending'], 6)
            self.assertEqual(len(replies[8]['result']['structuredContent']['stages']), 7)
            # Never overwrites, never leaves the workspace, never reads outside the lesson library.
            for i in (6, 10, 11, 12):
                self.assertTrue(replies[i]['result']['isError'], replies[i])
            self.assertIn('outside the workspace', replies[10]['result']['content'][0]['text'])
            self.assertFalse((workspace.parent / 'escape').exists())
            self.assertTrue((workspace / 'overview.html').is_file())


class RemoteServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ['FIEVEL_CHALLENGE_PATH'] = '/.well-known/challenge.txt'
        os.environ['FIEVEL_CHALLENGE_TOKEN'] = 'token-123'
        cls.httpd = ThreadingHTTPServer(('127.0.0.1', 0), mcp_remote.Handler)
        cls.httpd.RequestHandlerClass.log_message = lambda *a: None
        cls.base = f'http://127.0.0.1:{cls.httpd.server_address[1]}'
        threading.Thread(target=cls.httpd.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()
        for key in ('FIEVEL_CHALLENGE_PATH', 'FIEVEL_CHALLENGE_TOKEN'):
            os.environ.pop(key, None)

    def request(self, method, path, body=None):
        data = body if isinstance(body, bytes) or body is None else json.dumps(body).encode('utf-8')
        req = urllib.request.Request(self.base + path, data=data, method=method, headers={'Content-Type': 'application/json'})
        try:
            with urllib.request.urlopen(req) as res:
                return res.status, res.read().decode('utf-8'), res.headers
        except urllib.error.HTTPError as err:
            return err.code, err.read().decode('utf-8'), err.headers

    def mcp(self, message):
        status, body, _ = self.request('POST', '/mcp', message)
        self.assertEqual(status, 200, body)
        return json.loads(body)

    def test_stateless_tools(self):
        tools = {t['name'] for t in self.mcp({'jsonrpc': '2.0', 'id': 1, 'method': 'tools/list'})['result']['tools']}
        self.assertEqual(tools, {'fievel_list_lessons', 'fievel_get_lesson', 'fievel_get_template', 'fievel_get_schema',
                                 'fievel_validate_package', 'fievel_check_responses'})
        tool_defs = self.mcp({'jsonrpc': '2.0', 'id': 1, 'method': 'tools/list'})['result']['tools']
        self.assertTrue(all(t['annotations']['readOnlyHint'] and not t['annotations']['openWorldHint'] for t in tool_defs))
        valid = self.mcp(call(2, 'fievel_validate_package', {'package': PACKAGE, 'require_coverage': True}))['result']
        self.assertFalse(valid['isError'])
        self.assertEqual(valid['structuredContent']['system_scope'], 'content')
        report = self.mcp(call(3, 'fievel_check_responses', {'package': PACKAGE, 'responses': BAD}))['result']['structuredContent']['report']
        self.assertEqual(report['summary'], {'pass': 0, 'fail': 3, 'not_run': 6})
        broken = json.loads(json.dumps(PACKAGE))
        broken['standards']['rules'][0]['source_ids'] = ['missing-source']
        self.assertTrue(self.mcp(call(4, 'fievel_validate_package', {'package': broken}))['result']['isError'])
        self.assertTrue(self.mcp(call(5, 'fievel_validate_package', {'package': {'product': {}}}))['result']['isError'])
        template = self.mcp(call(6, 'fievel_get_template', {}))['result']['structuredContent']
        self.assertEqual(sorted(template['files']), sorted(f'{n}.json' for n in FILES))

    def test_http_boundaries(self):
        self.assertEqual(self.request('GET', '/mcp')[0], 405)
        self.assertEqual(self.request('POST', '/mcp', {'jsonrpc': '2.0', 'method': 'notifications/initialized'})[0], 202)
        self.assertEqual(self.request('POST', '/mcp', [{'jsonrpc': '2.0', 'id': 1, 'method': 'ping'}])[0], 400)
        self.assertEqual(self.request('POST', '/mcp', b'{not json')[0], 400)
        self.assertEqual(self.request('POST', '/mcp', b'{"a":1,"a":2}')[0], 400)
        self.assertEqual(self.request('POST', '/mcp', b' ' * (mcp_remote.MAX_BODY + 1))[0], 413)
        self.assertEqual(self.request('POST', '/elsewhere', {})[0], 404)
        status, body, headers = self.request('GET', '/.well-known/challenge.txt')
        self.assertEqual((status, body), (200, 'token-123'))
        self.assertTrue(headers['Content-Type'].startswith('text/plain'))
        status, body, headers = self.request('GET', '/health')
        self.assertEqual(status, 200)
        self.assertEqual(headers['Cache-Control'], 'no-store')
