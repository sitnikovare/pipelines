#!/bin/bash
cd test
poetry run pytest .
python cleanup.py

cd ..
cd example_pipeline
poetry run pipeline run
