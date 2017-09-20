FROM ubuntu:16.04

RUN \
  apt-get update && \
  apt-get install -y build-essential lsb-release git \
                     python python-pip \
                     uwsgi uwsgi-plugin-python

RUN pip install --upgrade pip

RUN pip install flask
RUN pip install Flask-HTTPAuth
RUN pip install dulwich
RUN pip install sqlalchemy
RUN pip install pyjwt
RUN pip install flask-bcrypt


RUN mkdir -p /app
RUN mkdir -p /data

WORKDIR /app


CMD uwsgi --http-socket :3447 --plugin python --pythonpath services --enable-threads --wsgi-file services/app.py --callable app
