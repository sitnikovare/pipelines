# Pipelines project

## How to run:
1. Init poetry
2. Get list of pipeline with
```
poetry run pipeline list
```

Output (fake for now):
```
INFO: function pipelines_list
```

3. Run pipeline in current directory with 

```
poetry run pipeline run
```

Output (fake for now):

```
INFO: pipelines started
        ...
INFO: pipelines finished
```

## CLI commands info
If you run command
```
poetry run pipeline
```

you can see next output:
```
Usage: pipeline [OPTIONS] COMMAND [ARGS]...

  Working with pipeline.

Options:
  --help  Show this message and exit.

Commands:
  list  - Get list of pipelines.
  run   - Run pipeline in current directory.
```