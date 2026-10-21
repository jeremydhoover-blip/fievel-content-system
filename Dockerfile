# Fievel remote MCP server for Google Cloud Run. Stateless; stores and logs no content.
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY VERSION ./
COPY scripts/fievel.py scripts/mcp_protocol.py scripts/mcp_tools.py scripts/mcp_remote.py scripts/
COPY schemas/ schemas/
COPY templates/content-system/ templates/content-system/
COPY examples/wayfarer/ examples/wayfarer/
COPY knowledge/ knowledge/
RUN useradd --system --no-create-home fievel
USER fievel
CMD ["python", "scripts/mcp_remote.py"]
