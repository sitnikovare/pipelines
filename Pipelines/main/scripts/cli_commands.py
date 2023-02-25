import click
from main.pipelines_scripts import main_commands


@click.group()
def pipeline():
    """ Working with pipeline. """
    pass


@pipeline.command()
def run():
    # click.echo("CLICK: command run started")
    """ - Run pipeline in current directory. """
    main_commands.pipelines_run()


@pipeline.command()
def list():
    # click.echo("CLICK: command list started")
    """ - Get list of pipelines. """
    main_commands.pipelines_list()

