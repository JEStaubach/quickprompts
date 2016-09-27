# -*- coding: utf-8 -*-

from quickprompts.selector import Selector
from quickprompts.widgets import SelectorFrame
from quickprompts.selector_view_model import SelectorViewModel
from quickprompts.common.util import Util

import click

@click.group()
def cli():
    """
    A utility for common tasks of prompting users for data.
    """

@click.option("--delim", default="::", help="Option hierarchy delimeter")
@click.option("--src", default="-", help="Source to read from for the list of options")
@click.option("--dest", default="-", help="Destination to print the selected options")
@cli.command()
def selector(delim,src,dest):
    """
    Select options from a list. Uses a path delimeter if the options are organized hierarchically.

    Example: quickprompts selector --src https://testpypi.python.org/pypi?%3Aaction=list_classifiers
    """
    click.echo("%s %s %s" % (delim,src,dest))
    svm = SelectorViewModel(Util.get_classifiers())
    selector = Selector(svm)
    selector.display()


if __name__ == "__main__":
    cli()
