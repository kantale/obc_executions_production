# VERSION 1.10.9
# AUTHOR: Manos Koutoulakis
# DESCRIPTION: Basic Airflow container(Version 1.10.9 ) with OBC-Client in it 
# BUILD: docker build --rm -t manoskoutoulakis/docker-obc-airflow .
# SOURCE: https://github.com/manoskout/docker-obc-airflow

FROM python:3.7-slim-buster
LABEL maintainer="Koutoulakis"

# Never prompt the user for choices on installation/configuration of packages
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

# Airflow
ARG AIRFLOW_VERSION=1.10.9
ARG AIRFLOW_USER_HOME=/usr/local/airflow
ARG AIRFLOW_DEPS=""
ARG PYTHON_DEPS=""
ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}

# Define en_US.
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8
ENV LC_MESSAGES en_US.UTF-8

# Disable noisy "Handling signal" log messages:
# ENV GUNICORN_CMD_ARGS --log-level WARNING

RUN set -ex \
    && buildDeps=' \
        freetds-dev \
        libkrb5-dev \
        libsasl2-dev \
        libssl-dev \
        libffi-dev \
        libpq-dev \
        git \
    ' \
    && apt-get update -yqq \
    && apt-get upgrade -yqq \
    && apt-get install -yqq --no-install-recommends \
        $buildDeps \
        freetds-bin \
	file \
        build-essential \
        default-libmysqlclient-dev \
        apt-utils \
        curl \
	wget \
	unzip \
        rsync \
        netcat \
        locales \
	vim \
    && sed -i 's/^# en_US.UTF-8 UTF-8$/en_US.UTF-8 UTF-8/g' /etc/locale.gen \
    && locale-gen \
    && update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 \
    && useradd -ms /bin/bash -d ${AIRFLOW_USER_HOME} airflow \
    && pip install -U pip setuptools wheel \
    && pip install pytz \
    && pip install pyOpenSSL \
    && pip install ndg-httpsclient \
    && pip install pyasn1 \
    && pip install apache-airflow[crypto,celery,postgres,hive,jdbc,mysql,ssh${AIRFLOW_DEPS:+,}${AIRFLOW_DEPS}]==${AIRFLOW_VERSION} \
    && pip install prometheus_client \
    && pip install 'redis==3.2' \
    && if [ -n "${PYTHON_DEPS}" ]; then pip install ${PYTHON_DEPS}; fi \
    && apt-get purge --auto-remove -yqq $buildDeps \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base

COPY script/entrypoint.sh /entrypoint.sh
#COPY config/airflow.cfg ${AIRFLOW_USER_HOME}/airflow.cfg

RUN chown -R airflow: ${AIRFLOW_USER_HOME}


# This fixes permission issues on linux. 
# The airflow user should have the same UID as the user running docker on the host system.
ARG DOCKER_UID
RUN \
    : "${DOCKER_UID:?Build argument DOCKER_UID needs to be set and non-empty. Use 'make build' to set it automatically.}" \
    && usermod -u ${DOCKER_UID} airflow \
    && echo "Set airflow's uid to ${DOCKER_UID}"

#USER airflow
#Set OBC_Client
RUN mkdir -m755 ${AIRFLOW_USER_HOME}/dags
RUN mkdir -m755 ${AIRFLOW_USER_HOME}/REPORTS
RUN mkdir -m755 ${AIRFLOW_USER_HOME}/REPORTS/WORK
RUN mkdir -m755 ${AIRFLOW_USER_HOME}/REPORTS/TOOL
RUN mkdir -m755 ${AIRFLOW_USER_HOME}/REPORTS/DATA

WORKDIR ${AIRFLOW_USER_HOME}
ENV FLASK_APP client.py
ENV FLASK_RUN_HOST 0.0.0.0

COPY /client/requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY /client/static/ ${AIRFLOW_USER_HOME}/static
COPY /client/templates/ ${AIRFLOW_USER_HOME}/templates
COPY /client/client.py ${AIRFLOW_USER_HOME}/

# Temporary sollution
RUN mkdir -m755 ${AIRFLOW_USER_HOME}/logs
RUN mkdir -m755 ${AIRFLOW_USER_HOME}/logs/compressed_logs
# RUN  -m777 ${AIRFLOW_USER_HOME}
ENTRYPOINT ["/entrypoint.sh"]
CMD ["webserver"]
