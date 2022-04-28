FROM python:3.6-slim-buster

# python envs
ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  CPLUS_INCLUDE_PATH=/usr/include/gdal \
  C_INCLUDE_PATH=/usr/include/gdal \
  GDAL_DATA=/usr/share/gdal \
  PROJ_LIB=/usr/share/proj

# Install spatial libraries to work with Postgis and Geodjango
RUN apt-get update -y && apt-get -y install build-essential binutils libproj-dev gdal-bin python-gdal libgdal-dev libtiff-tools gettext libtiff5 graphviz libgraphviz-dev

# python dependencies
COPY ./requirements /requirements
RUN pip install -r /requirements/production.txt

## Add the wait script to the image
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.6.0/wait /wait
RUN chmod +x /wait

# upload scripts
COPY ./compose/scripts/gunicorn.sh /

WORKDIR /app
