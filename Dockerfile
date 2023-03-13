FROM python:3.11.2 as base

ENV PYTHONUNBUFFERED 1

WORKDIR /pipelines

COPY ./ ./

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

ENTRYPOINT ["python", "example_pipeline/pipeline.py"]