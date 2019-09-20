#############################################################################
# NOTE: FILE GENERATED AUTOMATICALLY, DO NOT EDIT!!!
#############################################################################

FROM python:3.7-alpine

MAINTAINER Paweł Tomulik <ptomulik@meil.pw.edu.pl>

ARG KRW_CODE='/code'
ARG SPHINX_VERSION='2.2.0'
ARG SPHINX_AUTOBUILD_VERSION='0.7.1'
ARG SPHINX_RTD_THEME_VERSION='0.4.3'
ARG SPHINX_BREATHE_VERSION='4.13.1'
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


ENV KRW_CODE=$KRW_CODE \
    SPHINX_VERSION=$SPHINX_VERSION \
    SPHINX_AUTOBUILD_VERSION=$SPHINX_AUTOBUILD_VERSION \
    SPHINX_RTD_THEME_VERSION=$SPHINX_RTD_THEME_VERSION \
    SPHINX_BREATHE_VERSION=$SPHINX_BREATHE_VERSION \
    SPHINX_AUTOBUILD_HOST=$SPHINX_AUTOBUILD_HOST \
    SPHINX_AUTOBUILD_PORT=$SPHINX_AUTOBUILD_PORT \
    SPHINX_AUTOBUILD_FLAGS=$SPHINX_AUTOBUILD_FLAGS \
    SPHINX_BUILD_FLAGS=$SPHINX_BUILD_FLAGS \
    SPHINX_SOURCE_DIR=$SPHINX_SOURCE_DIR \
    SPHINX_BUILD_DIR=$SPHINX_BUILD_DIR

RUN set -xe && \
    apk add --no-cache --update git doxygen && \
    python -m pip install -U pip && \
    python -m pip install -U virtualenv && \
    python -m pip install sphinx=="${SPHINX_VERSION}" \
                          sphinx-autobuild=="${SPHINX_AUTOBUILD_VERSION}" \
                          sphinx_rtd_theme=="${SPHINX_RTD_THEME_VERSION}" \
                          "git+https://github.com/korowai/sphinx-php.git@korowai" \
                          breathe=="${SPHINX_BREATHE_VERSION}" && \
   rm -rf ~/.cache/pip && \
   mkdir -p $KRW_CODE

COPY bin/* /usr/local/bin/

EXPOSE $SPHINX_AUTOBUILD_PORT

VOLUME $KRW_CODE
WORKDIR $KRW_CODE

ENTRYPOINT [ "sphinx-entrypoint" ]
CMD ["autobuild"]

# vim: ft=dockerfile:
