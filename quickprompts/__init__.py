""" quickprompts module

The quickprompts module utilizes asciimatics to provide a curses interface
for common cases where information must be retrived from the user, such as
prompting for configuration values during setup and installation routines.

.. moduleauthor:: Justin Staubach <justin@staubach.us>

"""
from quickprompts.selector.selector import Selector
from quickprompts.selector.selector_view_model import SelectorViewModel
from .common import Util





