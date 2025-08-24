FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
ENV PORT=8082 DATA_DIR=/data
RUN mkdir -p /data && useradd -u 10001 appuser && chown -R appuser /data
USER appuser
EXPOSE 8082
CMD ["uvicorn","app:app","--host","0.0.0.0","--port","8082"]
