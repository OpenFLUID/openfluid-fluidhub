FROM ubuntu:16.04

RUN \
  apt-get update && \
  apt-get install -y build-essential lsb-release git \
                     python python-pip \
                     uwsgi uwsgi-plugin-python \
                     curl wget

RUN pip install --upgrade pip

RUN pip install requests
RUN pip install sh
RUN pip install pyjwt
RUN pip install nose


RUN mkdir -p /fluidhub
RUN mkdir -p /tests
RUN mkdir -p /_dev


RUN git config --global user.email "contact@openfluid-project.org"
RUN git config --global user.name "OpenFLUID project"


WORKDIR /tests
