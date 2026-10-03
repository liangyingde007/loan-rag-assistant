FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements-deploy.txt ./
RUN pip install --no-cache-dir -r requirements-deploy.txt \
    && useradd --create-home --uid 10001 appuser
COPY backend/main.py backend/serve.py ./backend/
COPY rag/loader.py rag/splitter.py rag/retriever.py rag/generator.py rag/pipeline.py ./rag/
COPY knowledge_base/demo_rules.json ./knowledge_base/demo_rules.json
COPY web ./web
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=15s --retries=3 \
    CMD python -c "import os, urllib.request; urllib.request.urlopen('http://127.0.0.1:' + os.getenv('PORT', '8000') + '/healthz', timeout=2)"
CMD ["python", "-m", "backend.serve"]
