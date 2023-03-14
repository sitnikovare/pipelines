FROM python:3.11.2

ENV PYTHONUNBUFFERED=1

RUN mkdir /pipelines
WORKDIR /pipelines
RUN mkdir /pipelines/pipelines

# COPY pyproject.toml /pipelines
# COPY poetry.lock /pipelines
# COPY setup.py /pipelines
# COPY README.md /pipelines
# COPY /pipelines /pipelines/pipelines
# COPY /example_pipeline /pipelines/example_pipeline

COPY . /pipelines

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

ENTRYPOINT [ "python", "example_pipeline/pipeline.py"]