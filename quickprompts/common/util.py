import requests

class Util:

    # Properties

    # Magic Methods

    def __init__(self, test=False):
        self._test = test

    # Public Methods

    @staticmethod
    def get_classifiers(test=False):
        classifiers_url = 'https://pypi.python.org/pypi?%3Aaction=list_classifiers'
        if test:
            classifiers_url = 'https://testpypi.python.org/pypi?%3Aaction=list_classifiers'
        r = requests.get(classifiers_url)
        return r.content.decode()

    @staticmethod
    def str_ends_in_substr(searchstring, searchval):
        return searchval == searchstring[-1 * len(searchval):]

    # Private Methods
