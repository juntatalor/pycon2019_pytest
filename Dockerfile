FROM python:3.7.3-alpine3.9

RUN apk add --no-cache \
        postgresql \
        python3-dev \
        postgresql-dev \
    && apk add --no-cache --virtual .build-deps \
        build-base

WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

RUN apk del .build-deps