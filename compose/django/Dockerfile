FROM python:slim-buster
RUN set -e

ENV VIRTUAL_ENV=/env \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt /

RUN apt update && apt install -y --fix-missing \
    build-essential \
    python3-dev \
    python3-pip \
    python3-venv \
    python3-pip \
    python3-dev \
    libpq-dev \
    apt-transport-https

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /usr/src/app

COPY ./ ./

EXPOSE 8000

# server/Dockerfile

# pull official base image
# FROM python:3.10

# # set working directory
# WORKDIR /usr/src/app

# # set environment variables
# ENV PYTHONUNBUFFERED 1
# ENV PYTHONDONTWRITEBYTECODE 1

# # install dependencies
# COPY ./requirements.txt .
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt