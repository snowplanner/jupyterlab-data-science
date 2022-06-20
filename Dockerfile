FROM jupyter/scipy-notebook

USER root

RUN apt-get update
RUN apt-get install build-essential software-properties-common -y
RUN apt-get install pkg-config

RUN jupyter nbextension enable --py widgetsnbextension
RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager @jupyterlab/geojson-extension

RUN apt-get install -y libspatialindex-dev

# RUN apt-get install gdal-bin libgdal-dev python3-gdal -y
RUN apt-get install gdal-bin -y && apt-get install libgdal-dev -y
RUN export CPLUS_INCLUDE_PATH=/usr/include/gdal && export C_INCLUDE_PATH=/usr/include/gdal

USER jovyan

COPY . /tmp/
RUN pip install --requirement /tmp/requirements.txt
