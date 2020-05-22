FROM python:3.7.4-alpine3.10

ADD django_project/requirements.txt /app/requirements.txt


RUN set -ex \
    && apk add --no-cache --virtual .build-deps postgresql-dev build-base \
    && apk add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev \
    && python -m venv /env \
    && apk add --no-cache libressl-dev musl-dev libffi-dev \
    && /env/bin/pip install --upgrade pip \
    && /env/bin/pip install --no-cache-dir cryptography==2.1.4 \
    && /env/bin/pip install --no-cache-dir -r /app/requirements.txt \
    && runDeps="$(scanelf --needed --nobanner --recursive /env \
        | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
        | sort -u \
        | xargs -r apk info --installed \
        | sort -u)" \
    && apk add --virtual rundeps $runDeps \
    && apk del libressl-dev musl-dev libffi-dev \
    && apk del .build-deps \
    && apk del .pynacl_deps

ADD django_project /app
WORKDIR /app

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "django_project.wsgi:application"]