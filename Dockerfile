FROM python:latest

ENV PYTHONIOENCODING=utf-8
ENV LANG=C.UTF-8
ENV TB_SERVER_ADDRESS ""
ENV REPORT_INTERVAL ""
LABEL authors="tomer.klein@gmail.com"

RUN apt -yqq update && \
    apt -yqq install fping && \
    rm -rf /var/lib/apt/lists/*
    
RUN pip install --upgrade pip --no-cache-dir && \
    pip install --upgrade setuptools --no-cache-dir && \
    pip install --upgrade pyyaml requests loguru schedule

RUN mkdir -p /app/config

COPY app /app

WORKDIR /app

ENTRYPOINT python app.py