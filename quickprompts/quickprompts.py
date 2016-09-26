# -*- coding: utf-8 -*-
from .selector_view_model import SelectorViewModel
from .selector import Selector
from .common.util import Util

import click


@click.group()
def cli():
    """
    A utility for common tasks of prompting users for data.
    """


@click.option("--delim", default="::", help="Option hierarchy delimeter")
@click.option("--src",
              default="-",
              help="Source to read from for the list of options")
@click.option("--dest",
              default="-",
              help="Destination to print the selected options")
@cli.command()
def selector(delim, src, dest):
    """
    Select options from a list. Uses a path delimeter if the options
    are organized hierarchically.
    """
    click.echo("%s %s %s" % (delim, src, dest))
    svm = SelectorViewModel(Util.get_classifiers())
    selector = Selector(svm)
    selector.display()


if __name__ == "__main__":
    cli()
