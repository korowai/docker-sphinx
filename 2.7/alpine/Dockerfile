FROM python:2.7-alpine

MAINTAINER Paweł Tomulik <ptomulik@meil.pw.edu.pl>

ARG SPHINX_UID=1000
ARG SPHINX_GID=1000
ARG SPHINX_VERSION='1.7.1'
ARG SPHINX_AUTOBUILD_VERSION='0.7.1'
ARG SPHINX_RTD_THEME_VERSION='0.4.2'
ARG SPHINX_AUTOBUILD_HOST='0.0.0.0'
ARG SPHINX_AUTOBUILD_PORT=8000
ARG SPHINX_AUTOBUILD_FLAGS=''
ARG SPHINX_BUILD_FLAGS=''
ARG SPHINX_SOURCE_DIR='docs/sphinx'
ARG SPHINX_BUILD_DIR='docs/build/html'

ARG BUILD_DATE
ARG VCS_REF
ARG VERSION

LABEL org.label-schema.build-date="${BUILD_DATE}" \
      org.label-schema.name="Docker Sphinx Image" \
      org.label-schema.description="Docker image with Sphinx documentation generator. Designed to build docs for Korowai project." \
      org.label-schema.vcs-ref="${VCS_REF}" \
      org.label-schema.vcs-url="https://github.com/korowai/docker-sphinx" \
      org.label-schema.vendor="Paweł Tomulik" \
      org.label-schema.version="${VERSION}" \
      org.label-schema.schema-version="1.0"


ENV SPHINX_UID=$SPHINX_UID \
    SPHINX_GID=$SPHINX_GID \
    SPHINX_VERSION=$SPHINX_VERSION \
    SPHINX_AUTOBUILD_VERSION=$SPHINX_AUTOBUILD_VERSION \
    SPHINX_RTD_THEME_VERSION=$SPHINX_RTD_THEME_VERSION \
    SPHINX_AUTOBUILD_HOST=$SPHINX_AUTOBUILD_HOST \
    SPHINX_AUTOBUILD_PORT=$SPHINX_AUTOBUILD_PORT \
    SPHINX_AUTOBUILD_FLAGS=$SPHINX_AUTOBUILD_FLAGS \
    SPHINX_BUILD_FLAGS=$SPHINX_BUILD_FLAGS \
    SPHINX_SOURCE_DIR=$SPHINX_SOURCE_DIR \
    SPHINX_BUILD_DIR=$SPHINX_BUILD_DIR

RUN set -xe && \
  addgroup -g $SPHINX_GID sphinx && \
  adduser -D -s /bin/sh -G sphinx -u $SPHINX_UID sphinx && \
  apk add --no-cache --update git

COPY bin/* /usr/local/bin/

USER sphinx

RUN (python -m venv ~/.venv || (python -m pip install --user -U virtualenv && ~/.local/bin/virtualenv ~/.venv)) && \
    . ~/.venv/bin/activate && \
    python -m pip install -U pip && \
    python -m pip install sphinx=="${SPHINX_VERSION}" \
                          sphinx-autobuild=="${SPHINX_AUTOBUILD_VERSION}" \
                          sphinx_rtd_theme=="${SPHINX_RTD_THEME_VERSION}" \
                          "git+https://github.com/fabpot/sphinx-php.git@7312ecc#egg_name=sphinx-php" && \
   rm -rf ~/.cache/pip


EXPOSE $SPHINX_AUTOBUILD_PORT

VOLUME /home/sphinx/project
WORKDIR /home/sphinx/project

ENTRYPOINT [ "sphinx-entrypoint" ]
CMD ["autobuild"]

# vim: ft=dockerfile:
