FROM continuumio/miniconda3 AS build

COPY environment.yml .
RUN conda env create -f environment.yml

RUN conda install --override-channels -c conda-forge conda-pack

RUN conda-pack -n mapping -o /tmp/env.tar && \
    mkdir /venv && cd /venv && tar xf /tmp/env.tar && \
    rm /tmp/env.tar

RUN /venv/bin/conda-unpack

FROM debian:buster AS runtime

COPY --from=build /venv /venv

ADD data ./data

ADD utils ./utils

ADD main.py .

SHELL ["/bin/bash", "-c"]	

ENTRYPOINT source /venv/bin/activate && \
	python main.py
