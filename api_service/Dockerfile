# syntax=docker/dockerfile:1
FROM python:3.10
RUN apt-get update -y && apt-get install apt-utils wait-for-it -y --no-install-recommends
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /api_service
COPY requirements.txt /api_service/
RUN pip install -r requirements.txt
COPY . /api_service/

