FROM continuumio/miniconda3

RUN conda install --override-channels -c conda-forge conda-pack

COPY environment.yml .
RUN conda env create -n tmpenv -f environment.yml

RUN conda-pack -n tmpenv -o /tmp/env.tar && \
    mkdir /venv && cd /venv && tar xf /tmp/env.tar && \
    rm /tmp/env.tar

RUN /venv/bin/conda-unpack

COPY main.py dockerised
