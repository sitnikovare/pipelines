FROM python:3.11.2

ENV PYTHONUNBUFFERED=1

RUN mkdir /pipelines
WORKDIR /pipelines
RUN mkdir /pipelines/pipelines

COPY . /pipelines

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

ENTRYPOINT [ "bash", "test_pipelines.sh"]

ENTRYPOINT [ "bash", "start_poetry.sh"]