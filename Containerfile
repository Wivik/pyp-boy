FROM python:3-slim

RUN apt-get update -y && apt-get clean

RUN groupadd pypboy && useradd -g pypboy -m -d /pypboy pypboy

USER pypboy

ADD --chown=pypboy:pypboy ./ /pypboy

RUN pip install --upgrade pip && pip install -r /pypboy/requirements.txt --user

VOLUME /pypboy/data

EXPOSE 5000

WORKDIR /pypboy

ENV FLASK_APP=app.py

ENTRYPOINT [ "python", "-m", "flask", "run", "--host", "0.0.0.0" ]

