import os

import click 


def _print_dir_content():
    contents = os.listdir(os.curdir)
    click.echo(contents)

def add_content_to_file(file_name: str, content: str):
    with open(f"{file_name}.txt", 'w') as f:
        f.write(content)

@click.group()
def cli():
    pass

@click.command()
@click.argument('file_name')
@click.option('--content', default="Demo Dag Content", help='some dummy conent')
def write(file_name, content):
    click.echo('Initialized the file')
    add_content_to_file(file_name, content)


@click.command()
def ls():
    click.echo('Content of current directory')
    _print_dir_content()


cli.add_command(write)
cli.add_command(ls)




if __name__ == '__main__':
    cli()
