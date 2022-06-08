import click

from .scrape import scrape


@click.argument('query')
@click.argument('region')
@click.command()
def cscrape(region: str, query: str):
    '''
    Search a Craiglist region for specific search term(s).
    '''
    results = scrape(region=region, query=query)
    for result in results:
        click.echo(result)
