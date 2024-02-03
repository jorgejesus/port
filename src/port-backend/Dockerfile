# Use Python 3.10.12 as the base image
# docker build --progress=plain --no-cache -t port-backend .
# docker run -p8000:8000
FROM docker.io/library/python:3.10.12-slim-bookworm@sha256:13cc673c11ee90d6ba92d95f35f4d8e59148937f1e3b4044788e93268bfe9d2e

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install tini to avoud PID=1 problems
RUN apt-get update && apt-get install -y --no-install-recommends tini && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

COPY . /app

# Base container is running as root
RUN chown -R www-data:www-data /app
USER www-data

ENTRYPOINT ["/usr/bin/tini", "--"]
# Command to run the application using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Or setting up the port but less secure with CMD
#ENV UVICORN_PORT=8000
#CMD uvicorn main:app --host 0.0.0.0 --port $UVICORN_PORT
