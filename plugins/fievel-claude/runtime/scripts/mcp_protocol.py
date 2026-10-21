"""Minimal Model Context Protocol (MCP) message handling shared by Fievel's servers.

Implements the JSON-RPC 2.0 methods a tools-only server needs: initialize, ping,
tools/list and tools/call. No dependencies, no network access and no model calls.
"""
import json

SUPPORTED_VERSIONS = ('2025-06-18', '2025-03-26', '2024-11-05')
PARSE_ERROR, INVALID_REQUEST, METHOD_NOT_FOUND, INVALID_PARAMS, INTERNAL_ERROR = -32700, -32600, -32601, -32602, -32603


class Tool:
    """A named tool with a JSON Schema for its arguments and a handler returning JSON data."""

    def __init__(self, name, title, description, properties, required, handler, read_only=True):
        self.name, self.handler = name, handler
        self.definition = {
            'name': name, 'title': title, 'description': description,
            'inputSchema': {'type': 'object', 'properties': properties,
                            'required': list(required), 'additionalProperties': False},
            'annotations': {'title': title, 'readOnlyHint': read_only, 'destructiveHint': False,
                            'idempotentHint': read_only, 'openWorldHint': False},
        }


def _error(request_id, code, message):
    return {'jsonrpc': '2.0', 'id': request_id, 'error': {'code': code, 'message': message}}


def _check_arguments(tool, arguments):
    schema = tool.definition['inputSchema']
    if not isinstance(arguments, dict):
        raise ValueError('Tool arguments must be an object.')
    unknown = set(arguments) - set(schema['properties'])
    missing = [name for name in schema['required'] if name not in arguments]
    if unknown:
        raise ValueError('Unknown argument(s): ' + ', '.join(sorted(unknown)))
    if missing:
        raise ValueError('Missing argument(s): ' + ', '.join(missing))
    kinds = {'string': str, 'boolean': bool, 'object': dict, 'integer': int}
    for name, value in arguments.items():
        expected = kinds.get(schema['properties'][name].get('type'))
        if expected and (not isinstance(value, expected) or (expected is int and isinstance(value, bool))):
            raise ValueError(f'Argument {name} must be of type {schema["properties"][name]["type"]}.')


class Server:
    def __init__(self, name, version, instructions, tools):
        self.info = {'name': name, 'title': 'Fievel', 'version': version}
        self.instructions = instructions
        self.tools = {tool.name: tool for tool in tools}

    def handle(self, message):
        """Return the JSON-RPC response for one message, or None for a notification."""
        if not isinstance(message, dict) or message.get('jsonrpc') != '2.0' or not isinstance(message.get('method'), str):
            return _error(message.get('id') if isinstance(message, dict) else None, INVALID_REQUEST, 'Invalid JSON-RPC request.')
        if 'id' not in message:
            return None  # Notifications such as notifications/initialized need no reply.
        request_id, method, params = message['id'], message['method'], message.get('params') or {}
        if not isinstance(params, dict):
            return _error(request_id, INVALID_PARAMS, 'params must be an object.')
        if method == 'initialize':
            requested = params.get('protocolVersion')
            version = requested if requested in SUPPORTED_VERSIONS else SUPPORTED_VERSIONS[0]
            return {'jsonrpc': '2.0', 'id': request_id, 'result': {
                'protocolVersion': version, 'capabilities': {'tools': {'listChanged': False}},
                'serverInfo': self.info, 'instructions': self.instructions}}
        if method == 'ping':
            return {'jsonrpc': '2.0', 'id': request_id, 'result': {}}
        if method == 'tools/list':
            return {'jsonrpc': '2.0', 'id': request_id,
                    'result': {'tools': [tool.definition for tool in self.tools.values()]}}
        if method == 'tools/call':
            tool = self.tools.get(params.get('name'))
            if tool is None:
                return _error(request_id, INVALID_PARAMS, f'Unknown tool: {params.get("name")}')
            arguments = params.get('arguments', {})
            try:
                _check_arguments(tool, arguments)
                data = tool.handler(**arguments)
            except (ValueError, FileExistsError, FileNotFoundError, NotADirectoryError, IsADirectoryError, PermissionError) as exc:
                # Tool failures are results the agent can read and act on, not protocol errors.
                return {'jsonrpc': '2.0', 'id': request_id, 'result': {
                    'content': [{'type': 'text', 'text': f'Error: {exc}'}], 'isError': True}}
            except Exception as exc:  # A server must answer every request.
                return _error(request_id, INTERNAL_ERROR, f'{type(exc).__name__}: {exc}')
            return {'jsonrpc': '2.0', 'id': request_id, 'result': {
                'content': [{'type': 'text', 'text': json.dumps(data, ensure_ascii=False, indent=2)}],
                'structuredContent': data, 'isError': False}}
        return _error(request_id, METHOD_NOT_FOUND, f'Unknown method: {method}')
