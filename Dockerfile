FROM python:3.10

ENV PYTHONUNBUFFERED 1

RUN apt-get update

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /app
COPY ./app /app
WORKDIR /app

#CMD [ "tail", "-f", "/dev/null" ] 