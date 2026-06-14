# AI-KungFU East Africa MCP Server
# Glama-compatible Dockerfile for nishati-mcp
FROM python:3.12-slim

LABEL org.opencontainers.image.source="https://github.com/gabrielmahia/nishati-mcp"
LABEL org.opencontainers.image.description="nishati-mcp — East Africa AI Coordination Infrastructure"
LABEL org.opencontainers.image.licenses="MIT"

RUN pip install --no-cache-dir nishati-mcp

CMD ["nishati-mcp"]
