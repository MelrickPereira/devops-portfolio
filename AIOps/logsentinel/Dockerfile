FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY parser.py detector.py alerter.py .

ENTRYPOINT ["python", "detector.py"]
