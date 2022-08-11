FROM python:3.10-slim-bullseye

WORKDIR /code
ADD requirements.txt ./

RUN apt-get update
RUN apt-get -y install libpq-dev gcc
RUN apt-get -y install cron

RUN pip install -r requirements.txt

COPY crontab /var/spool/cron/crontabs/root
RUN crontab /var/spool/cron/crontabs/root

ENV AMQP_URL='amqp://rabbit_mq?connection_attempts=10&retry_delay=11'
ENV DB_HOST='localhost'
ENV DB_NAME='homestead'
ENV DB_PORT='5432'
ENV DB_USER='root'
ENV DB_PASS=''

ADD . .

CMD ["python3", "./main.py"]