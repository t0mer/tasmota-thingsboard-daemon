FROM python:latest

ENV PYTHONIOENCODING=utf-8
ENV LANG=C.UTF-8
ENV TB_SERVER_ADDRESS ""
ENV REPORT_INTERVAL ""
LABEL authors="tomer.klein@gmail.com"

RUN apt -yqq update && \
    apt -yqq install fping && \
    rm -rf /var/lib/apt/lists/*
    
RUN pip3 install --upgrade pip --no-cache-dir && \
    pip3 install --upgrade setuptools --no-cache-dir

RUN mkdir -p /app/config

COPY requirements.txt /tmp

RUN pip3 install -r /tmp/requirements.txt

COPY app /app

WORKDIR /app

ENTRYPOINT ["/usr/bin/python3", "/app/defauly.py"]