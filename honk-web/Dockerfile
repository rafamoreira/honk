FROM python:3.11-bookworm

RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    sqlite3

ENV PYTHONUNBUFFERED 1

RUN mkdir /app

WORKDIR /app

ADD . /app/

RUN pip install -r /app/requirements.txt
