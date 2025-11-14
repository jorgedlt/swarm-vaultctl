import click
import json
import yaml
from vault import Vault

@click.group()
@click.option('--config', default='/app/config/config.yaml', help='Config file path')
@click.pass_context
def cli(ctx, config):
    with open(config, 'r') as f:
        cfg = yaml.safe_load(f)
    master_key_file = cfg['encryption']['master_key_file']
    with open(master_key_file, 'r') as f:
        master_key = f.read().strip()
    storage_file = cfg['storage']['file']
    ctx.obj = Vault(master_key, storage_file)

@cli.command()
@click.argument('key')
@click.pass_obj
def get(vault, key):
    value = vault.get(key)
    click.echo(value)

@cli.command()
@click.argument('key')
@click.argument('value')
@click.pass_obj
def set(vault, key, value):
    vault.set(key, value)
    click.echo("Set")

@cli.command()
@click.argument('key')
@click.pass_obj
def delete(vault, key):
    success = vault.delete(key)
    click.echo("Deleted" if success else "Not found")

@cli.command()
@click.pass_obj
def list(vault):
    keys = vault.list_keys()
    click.echo('\n'.join(keys))

@cli.command()
@click.argument('new_key')
@click.pass_obj
def rotate(vault, new_key):
    vault.rotate_key(new_key)
    click.echo("Rotated")

@cli.command()
@click.pass_obj
def status(vault):
    stat = vault.status()
    click.echo(json.dumps(stat))

if __name__ == '__main__':
    cli()