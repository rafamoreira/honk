FROM python:3.11-bookworm

ENV PYTHONUNBUFFERED 1

RUN mkdir /app

WORKDIR /app

ADD . /app/

RUN pip install -r /app/requirements.txt
