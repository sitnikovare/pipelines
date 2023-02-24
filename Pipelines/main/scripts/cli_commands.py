import click
from main.pipelines_scripts import main_commands


@click.group()
def pipeline():
    pass


@pipeline.command()
def run():
    # click.echo("CLICK: command run started")
    main_commands.pipelines_run()


@pipeline.command()
def list():
    # click.echo("CLICK: command list started")
    main_commands.pipelines_list()

