FROM python:3.7-alpine

RUN apk update && apk upgrade
RUN apk add --update \
    python \
    python-dev \
    py-pip \
    build-base \
  && pip install virtualenv \
  && rm -rf /var/cache/apk/*
RUN apk --no-cache add libxml2-dev libxslt-dev libffi-dev openssl-dev python3-dev
RUN apk --no-cache add --virtual build-dependencies
RUN pip install -U gevent appkernel
RUN pip install -U money

WORKDIR /app
COPY ./checkout /app/checkout