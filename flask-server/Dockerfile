#FROM python:3.6.8-alpine3.9
FROM python:3.8-slim-buster

ENV GROUP_ID=1000 \
    USER_ID=1000

WORKDIR /var/www/

ADD . /var/www/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn

RUN addgroup -gid $GROUP_ID www
#RUN adduser -D -u $USER_ID -G www www -s /bin/sh
RUN adduser --disabled-password -u $USER_ID -gid $GROUP_ID www --shell /bin/sh

USER www

EXPOSE 5000
CMD gunicorn wsgi -w 4 -b 0.0.0.0:5000