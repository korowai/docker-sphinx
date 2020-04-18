# korowai/docker-sphinx

[![](https://img.shields.io/docker/stars/korowai/sphinx.svg)](https://hub.docker.com/r/korowai/sphinx/ "Docker Stars")
[![](https://img.shields.io/docker/pulls/korowai/sphinx.svg)](https://hub.docker.com/r/korowai/sphinx/ "Docker Pulls")

Docker container with [sphinx](http://sphinx-doc.org/) documentation generator.
The container is designed to build documentation for
[Korowai](https://github.com/korowai/korowai/) and
[Korowai Framework](https://github.com/korowai/framework/) out of the
box. It may be easily adjusted to support other projects.

## Image versions

  - [![](https://images.microbadger.com/badges/version/korowai/sphinx.svg)](https://microbadger.com/images/korowai/sphinx "Get your own version badge on microbadger.com") [![](https://images.microbadger.com/badges/image/korowai/sphinx.svg)](https://microbadger.com/images/korowai/sphinx "Get your own image badge on microbadger.com")
  - [![](https://images.microbadger.com/badges/version/korowai/sphinx:3.7-alpine.svg)](https://microbadger.com/images/korowai/sphinx:3.7-alpine "Get your own version badge on microbadger.com") [![](https://images.microbadger.com/badges/image/korowai/sphinx:3.7-alpine.svg)](https://microbadger.com/images/korowai/sphinx:3.7-alpine "Get your own image badge on microbadger.com")
  - [![](https://images.microbadger.com/badges/version/korowai/sphinx:3.6-alpine.svg)](https://microbadger.com/images/korowai/sphinx:3.6-alpine "Get your own version badge on microbadger.com") [![](https://images.microbadger.com/badges/image/korowai/sphinx:3.6-alpine.svg)](https://microbadger.com/images/korowai/sphinx:3.6-alpine "Get your own image badge on microbadger.com")
  - [![](https://images.microbadger.com/badges/version/korowai/sphinx:3.5-alpine.svg)](https://microbadger.com/images/korowai/sphinx:3.5-alpine "Get your own version badge on microbadger.com") [![](https://images.microbadger.com/badges/image/korowai/sphinx:3.5-alpine.svg)](https://microbadger.com/images/korowai/sphinx:3.5-alpine "Get your own image badge on microbadger.com")
  - [![](https://images.microbadger.com/badges/version/korowai/sphinx:2.7-alpine.svg)](https://microbadger.com/images/korowai/sphinx:2.7-alpine "Get your own version badge on microbadger.com") [![](https://images.microbadger.com/badges/image/korowai/sphinx:2.7-alpine.svg)](https://microbadger.com/images/korowai/sphinx:2.7-alpine "Get your own image badge on microbadger.com")

## Features

With this container you can:

  - build documentation once and exit,
  - build documentation continuously and serve it at the same time.

The default behavior is to build continuously and serve at the same time.

## Quick example

Assume we have the following file hierarchy (the essential here is assumption
that sphinx configuration file `conf.py` is found under `docs/sphinx`)

```console
user@pc:$ tree .
.
`-- docs
    `-- sphinx
        |-- conf.py
        `-- index.rst
```

### Running with docker

Run it as follows

```console
user@pc:$ docker run --rm -it -v "$(pwd):/code" -p 8000:8000 --user "`id -u`:`id -g`" korowai/sphinx
```

### Running with docker-compose

In the top level directory create `docker-compose.yml` containing the following

```yaml
version: '3'
# ....
services:
   # ...
   sphinx:
      image: korowai/sphinx
      ports:
         - "8000:8000"
      volumes:
         - ./:/code
      user: "1000:1000"
```

Then run

```console
user@pc:$ docker-compose up sphinx
```

### Results

Whatever method you chose to run the container, you shall see new directory

```console
user@pc:$ ls -d docs/build/*
docs/build/html
```

The documentation is written to `docs/build/html`

```console
user@pc:$ find docs -name 'index.html'
docs/build/html/index.html
```

As long as the container is running, the documentation is available at

  - <http://localhost:8000>.

## Customizing

Several parameters can be changed via environment variables, for example we can
change build directory to ``build/docs/html`` as follows

```console
user@pc:$ docker run --rm -it -v "$(pwd):/code" -p 8000:8000 -e SPHINX_BUILD_DIR=build/docs/html korowai/sphinx
```

## Details

### Volume mount points exposed

  - `/code` - bind top level directory of your project here.

This may be changed with the configuration variable

### Working directory

  - `/code`

### Files inside container

#### In `/usr/local/bin`

  - scripts which may be used as container's command:
      - `autobuild` - builds documentation continuously (watches source
        directory for changes) and runs http server,
      - `build` - builds documentation once and exits,
  - other files
      - `sphinx-defaults` - initializes `DEFAULT_SPHINX_xxx` variables (default
        values),
      - `sphinx-env` - initializes `SPHINX_xxx` variables,
      - `sphinx-entrypoint` - provides an entry point for docker.

### Build arguments & environment variables

The container defines several build arguments which are copied to corresponding
environment variables within the running container. Most of the
arguments/variables have names starting with `SPHINX_` prefix. All the scripts
respect these variables, so the easiest way to adjust the container to your
needs is to set environment variables (`-e` flag to [docker](https://docker.com/)).
`KRW_CODE` is an exception, it must be defined at build time.

| Argument                    | Default Value            | Description                                            |
| --------------------------- | ------------------------ | ------------------------------------------------------ |
| KRW\_CODE                   | /code                    | A predefined volume mountpoint and workdir.            |
| SPHINX\_UID                 | 1000                     | UID of the user running commands within the container. |
| SPHINX\_GID                 | 1000                     | GID of the user running commands within the container. |
| SPHINX\_VERSION             | 3.0.1                    | Version of sphinx to be installed (pypi).              |
| SPHINX\_AUTOBUILD\_VERSION  | 0.7.1                    | Version of sphinx-autobuild to be installed (pypi).    |
| SPHINX\_RTD\_THEME\_VERSION | 0.4.3                    | Version of sphinx\_rtd\_scheme to be installed (pypi). |
| SPHINX\_BREATHE\_VERSION    | 4.15.0                   | Version of breathe to be installed (pypi).             |
| SPHINX\_AUTOBUILD\_HOST     | 0.0.0.0                  | Host address for the listening socket for http server. |
| SPHINX\_AUTOBUILD\_PORT     | 8000                     | Port numer (within container) for the http server.     |
| SPHINX\_AUTOBUILD\_FLAGS    |                          | CLI flags for running sphinx-autobuild.                |
| SPHINX\_BUILD\_FLAGS        |                          | CLI flags for running sphinx-build.                    |
| SPHINX\_SOURCE\_DIR         | docs/sphinx              | Top-level directory conf.py for the sphinx docs.       |
| SPHINX\_BUILD\_DIR          | docs/build/html          | Where to output the generated documentation.           |

### Software included

  - [python](https://python.org/)
  - [git](https://git-scm.com/)
  - [sphinx](https://sphinx-doc.org/)

## LICENSE

Copyright (c) 2018-2020 by Paweł Tomulik <ptomulik@meil.pw.edu.pl>

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE
