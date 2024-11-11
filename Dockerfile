FROM python:3.10-slim-buster

RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /downloads

COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

COPY *.py /app/

# Set environment variable to disable output buffering
ENV PYTHONUNBUFFERED=1

ENTRYPOINT [ "python", "/app/main.py" ]