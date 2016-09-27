# -*- coding: utf-8 -*-
from quickprompts.common.util import Util


class SelectorViewModel(list):

    # Properties

    # Magic Methods

    def __init__(self, options):
        super(SelectorViewModel, self).__init__()
        self._model = SelectorViewModel.generate_model(options)
        self.bread_crumbs = []
        self._chldren_indicator = '>>'
        for item in self._format_options_list():
            self.append(item)

    # Public Methods

    @staticmethod
    def generate_model(options, delimiter='::'):
        d = {}
        lines = [line.strip() for line in options.split('\n') if line.strip()]
        for line in lines:
            sections = [x.strip() for x in line.split(delimiter) if x.strip()]
            d = SelectorViewModel._chomp(sections, d)
        return d

    def step_into_item(self, selected):
        if selected not in self:
            raise ValueError(str(selected) +
                             ' not found in SelectorViewModel')
        if Util.str_ends_in_substr(selected, self._chldren_indicator):
            selected_index = self.index(selected)
            options = self._get_options_list()
            options_text = sorted(options.keys())
            option_selected = options_text[selected_index]
            self.bread_crumbs.append(option_selected)
            del self[:]
            for item in self._format_options_list():
                self.append(item)

    def step_out_of_item(self):
        item_stepped_out_of = ''
        if self.bread_crumbs:
            item_stepped_out_of = self.bread_crumbs[-1]
            self.bread_crumbs.pop()
            del self[:]
            for item in self._format_options_list():
                self.append(item)
        return item_stepped_out_of

    # Private Methods

    @staticmethod
    def _chomp(sections, d):
        if sections:
            if sections[0] not in d:
                if sections[1:]:
                    d[sections[0]] = {}
                else:
                    d[sections[0]] = {'': {}}
            d[sections[0]] = SelectorViewModel._chomp(sections[1:],
                                                      d[sections[0]])
        return d

    def _format_options_list(self):
        options = self._get_options_list()
        options_text = sorted(options.keys())
        formatted_options = []
        for option_text in options_text:
            if self._get_children(options[option_text]):
                option_index = options_text.index(option_text)
                padding = self._get_padding(options_text, option_index)
                formatted_options.append(option_text +
                                         padding +
                                         self._chldren_indicator)
            else:
                formatted_options.append(option_text)
        return sorted(formatted_options)

    @staticmethod
    def _get_children(option_children):
        return [child for child in option_children.keys() if child]

    @staticmethod
    def _get_max_option_length(options):
        return max([len(x) for x in options])

    def _get_options_list(self):
        page = self._model
        for crumb in self.bread_crumbs:
            if crumb not in page.keys():
                raise ValueError(str(self.bread_crumbs) +
                                 ' : path traversal failed at ' +
                                 str(crumb))
            else:
                page = page[crumb]
        return page

    @staticmethod
    def _get_padding_amount(options, index):
        option = options[index]
        pad_to_length = SelectorViewModel._get_max_option_length(options) + 1
        return pad_to_length - len(option)

    @staticmethod
    def _get_padding(options, index):
        return ' ' * SelectorViewModel._get_padding_amount(options, index)
