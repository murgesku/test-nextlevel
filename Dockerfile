FROM python:3.10

ENV PYTHONBUFFERED 1

WORKDIR /code

COPY ./app/requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8080
