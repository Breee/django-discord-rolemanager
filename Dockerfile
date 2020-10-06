FROM python:3.9-alpine
LABEL maintainer="Breee@github"

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE pogobackend.settings

RUN apk --no-cache update && apk --no-cache upgrade && apk --no-cache add --virtual buildpack gcc musl-dev build-base
RUN apk --no-cache update && apk --no-cache add git postgresql-dev zlib-dev jpeg-dev tzdata binutils libc-dev

COPY ./pogobackend/requirements.txt /usr/src/app/requirements.txt
RUN pip install -r /usr/src/app/requirements.txt && pip install gunicorn

COPY pogobackend /usr/src/app
COPY entrypoint.sh /usr/src/app/entrypoint.sh
WORKDIR /usr/src/app

RUN apk del buildpack

RUN chmod +x /usr/src/app/entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
