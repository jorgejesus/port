# Intro

Dummy backend REST to accept port JSON payload, and append it to a file.  File can be retrieved to check the payload arrived.

For testing when docker is running.

```bash
curl -X 'POST'  \
'http://localhost:8000/append/' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{"name": "John Doe","age":30}'
```

