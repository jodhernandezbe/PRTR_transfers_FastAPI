FROM continuumio/miniconda3

LABEL mantainer="jodhernandezbemj@gmail.com"

WORKDIR /PRTR_transfers_FastAPI

SHELL ["/bin/bash", "--login", "-c"]

COPY fastapi_environment.yml /PRTR_transfers_FastAPI/
RUN conda env create --file fastapi_environment.yml

RUN conda init bash

RUN echo "conda activate fastapi_app" > ~/.bashrc
RUN echo "Make sure fastapi is installed:"
RUN python -c "import fastapi"

COPY ["data/base.py", "data/model.py", "/PRTR_transfers_FastAPI/data/"]
COPY data/output/PRTR_transfers_summary.db /PRTR_transfers_FastAPI/data/output/PRTR_transfers_summary.db
COPY /fastapi_app  /PRTR_transfers_FastAPI/fastapi_app/

ENV PYTHONPATH /PRTR_transfers_FastAPI
CMD python fastapi_app/main.py