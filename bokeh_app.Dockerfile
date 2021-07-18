FROM continuumio/miniconda3

LABEL mantainer="jodhernandezbemj@gmail.com"

WORKDIR /PRTR_transfers_FastAPI

SHELL ["/bin/bash", "--login", "-c"]

COPY bokeh_environment.yml /PRTR_transfers_FastAPI/
RUN conda env create --file bokeh_environment.yml

RUN conda init bash

RUN echo "conda activate bokeh_app" > ~/.bashrc
RUN echo "Make sure bokeh is installed:"
RUN python -c "import bokeh"

COPY __init__.py .
COPY data/base.py /PRTR_transfers_FastAPI/data/base.py
COPY data/output/PRTR_transfers_summary.db /PRTR_transfers_FastAPI/data/output/PRTR_transfers_summary.db
COPY ["bokeh_app/main.py", "bokeh_app/tab_1.py", "bokeh_app/tab_2.py", "bokeh_app/tab_3.py", "/PRTR_transfers_FastAPI/bokeh_app/"]

ENV PYTHONPATH /PRTR_transfers_FastAPI
CMD bokeh serve --port=5006 --address=0.0.0.0 --allow-websocket-origin=* bokeh_app