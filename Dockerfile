FROM python:3.6.6-jessie

LABEL maintainer "Alexander Konyukov <scor2k@gmail.com>"

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /opt/redis_keys_exporter 
WORKDIR /opt/redis_keys_exporter

EXPOSE 9210
ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0:9210 --timeout 60 --workers=1 --log-level=info"

COPY . .
RUN pip install -r requirements.txt

CMD [ "gunicorn", "main:api" ]

