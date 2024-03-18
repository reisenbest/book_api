FROM python:3.11-alpine3.16

COPY requirements.txt /temp/requirements.txt

COPY books_api_service /books_api_service

RUN chmod -R 777 /books_api_service

WORKDIR /books_api_service

EXPOSE 8000

EXPOSE 5432

RUN apk add postgresql-client build-base postgresql-dev

RUN pip install -r /temp/requirements.txt

RUN adduser -D service-user


USER service-user