FROM python:3.12-slim

# Fixed numeric UID/GID, no home directory, no login shell
RUN useradd --uid 10001 --no-create-home --shell /usr/sbin/nologin appuser

WORKDIR /app
COPY --chown=10001:10001 app.py .

ENV PYTHONUNBUFFERED=1

USER 10001:10001
EXPOSE 8000
CMD ["python3", "app.py"]