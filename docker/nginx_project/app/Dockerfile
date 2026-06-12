FROM python:3.11-alpine

WORKDIR /app

COPY app.py .

RUN apk add --no-cache wget && \
    addgroup -S appgroup && \
    adduser -S appuser -G appgroup && \
    pip install --no-cache-dir flask gunicorn

RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 5000

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]