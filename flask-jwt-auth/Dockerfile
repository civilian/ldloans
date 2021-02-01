FROM ubuntu:18.04 as base

RUN apt-get update

RUN apt-get -y install software-properties-common

RUN apt-get -y install python3.8

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 2

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.8 2

RUN apt-get -y install python3-pip

# RUN apt-get -y install postgresql

# RUN apt-get -y install python-psycopg2

# To fix Python.h includes and compilations

RUN apt-get -y install python3.8-dev

FROM base as with-requirements

ARG BASE_DIR

WORKDIR ${BASE_DIR}

COPY requirements.txt ${BASE_DIR}

RUN pip3 install -r requirements.txt

