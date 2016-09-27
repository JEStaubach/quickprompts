#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_quickprompts
----------------------------------

Tests for `quickprompts` module.
"""
from contextlib import contextmanager
#from click.testing import CliRunner

from quickprompts import quickprompts

# noinspection PyPackageRequirements
import pytest
from quickprompts.common.util import Util
from quickprompts.selector_view_model import SelectorViewModel

# noinspection PyClassHasNoInit
class TestExternal:

    @pytest.mark.webtest
    def test_retrieve_classifiers(self):
        classifiers = Util.get_classifiers(test=True)
        assert('Development Status :: 5 - Production/Stable' in classifiers)
        assert('Framework :: Pytest' in classifiers)
        assert('License :: OSI Approved :: MIT License' in classifiers)
        assert('Natural Language :: English' in classifiers)
        assert('Programming Language :: Python' in classifiers)
        assert('Topic :: Software Development' in classifiers)
        assert('Intended Audience :: Developers' in classifiers)

        svm = SelectorViewModel(classifiers)
        assert(len(svm._model.keys()) > 0)
        assert('Development Status' in svm._model.keys())


# noinspection PyClassHasNoInit
class TestMenuViewModel:

    @staticmethod
    def exercise_nav(test_input, nav_test):
        svm = SelectorViewModel(test_input)
        for options, bread_crumbs, command in nav_test:
            assert(svm == options)
            assert(svm.bread_crumbs == bread_crumbs)
            if command:
                if command == '<<':
                    svm.step_out_of_item()
                else:
                    svm.step_into_item(command)

    @staticmethod
    def check_menu_model(test_input, expected_value):
        sm = SelectorViewModel.generate_model(test_input)
        assert(sm == expected_value)
        assert(expected_value == sm)

    def test_chomp(self):
        test_input = ['foo', 'bar', 'cat', 'dog']
        expected_value = {'foo': {'bar': {'cat': {'dog': {'': {}}}}}}

        sm = SelectorViewModel._chomp(test_input, {})
        assert(sm == expected_value)

    def test_menu_view_model1(self):
        test_inputs = ['', '::']
        expected_value = {}
        nav_test = [([],[],'')]
        for test_input in test_inputs:
            TestMenuViewModel.check_menu_model(test_input, expected_value)
            TestMenuViewModel.exercise_nav(test_input, nav_test)

    def test_menu_view_model2(self):
        test_input = ' foo :: bar :: cat :: dog '
        expected_value = {'foo': {'bar': {'cat': {'dog': {'': {}}}}}}
        nav_test = [(['foo >>'], [], 'foo >>'),
                    (['bar >>'], ['foo'], 'bar >>'),
                    (['cat >>'], ['foo', 'bar'], 'cat >>'),
                    (['dog'], ['foo', 'bar', 'cat'], 'dog'),
                    (['dog'], ['foo', 'bar', 'cat'], '<<'),
                    (['cat >>'], ['foo', 'bar'], '<<'),
                    (['bar >>'], ['foo'], '<<'),
                    (['foo >>'], [], '<<'),
                    (['foo >>'], [], '')]
        TestMenuViewModel.check_menu_model(test_input, expected_value)
        TestMenuViewModel.exercise_nav(test_input, nav_test)

    def test_menu_view_model3(self):
        test_input = '\n'.join(['foo::bar::cat',
                                ' foo::bar::cat::dog'])
        expected_value = {'foo': {'bar': {'cat': {'': {},
                                                  'dog': {'': {}}}}}}
        TestMenuViewModel.check_menu_model(test_input, expected_value)

    def test_menu_view_model4(self):
        test_input = '\n'.join(['foo::bar::cat',
                                'foo::bar::cat::dog',
                                'foo::bar::cat::mouse',
                                'foo::bar::tool',
                                'foo::bar::tool::hammer',
                                'foo::bar::tool::screw driver'])
        expected_value = {'foo': {'bar': {'cat': {'': {},
                                                  'dog': {'': {}},
                                                  'mouse': {'': {}}},
                                          'tool': {'': {},
                                                   'hammer': {'': {}},
                                                   'screw driver': {'': {}}}}}}
        nav_test = [(['foo >>'], [], 'foo >>'),
                    (['bar >>'], ['foo'], 'bar >>'),
                    (['cat  >>',
                      'tool >>'], ['foo', 'bar'], 'cat  >>'),
                    (['',
                      'dog',
                      'mouse'], ['foo', 'bar', 'cat'], 'dog'),
                    (['',
                      'dog',
                      'mouse'], ['foo', 'bar', 'cat'], 'mouse'),
                    (['',
                      'dog',
                      'mouse'], ['foo', 'bar', 'cat'], '<<'),
                    (['cat  >>',
                      'tool >>'], ['foo', 'bar'], 'tool >>'),
                    (['',
                      'hammer',
                      'screw driver'], ['foo', 'bar', 'tool'], 'hammer'),
                    (['',
                      'hammer',
                      'screw driver'], ['foo', 'bar', 'tool'], 'screw driver')]
        TestMenuViewModel.check_menu_model(test_input, expected_value)
        TestMenuViewModel.exercise_nav(test_input, nav_test)

    def test_menu_view_model5(self):
        sm1 = SelectorViewModel.generate_model('foo::bar::cat')
        sm2 = SelectorViewModel.generate_model('foo::bar::cat::')
        sm3 = SelectorViewModel.generate_model('::foo::bar::cat')
        sm4 = SelectorViewModel.generate_model('foo::::bar::cat')
        assert(sm1 == sm2 == sm3 == sm4)

    def test_menu_view_model6(self):
        sm1 = SelectorViewModel.generate_model('foo,bar,cat', ',')
        sm2 = SelectorViewModel.generate_model('foo..bar..cat..', '..')
        sm3 = SelectorViewModel.generate_model(' foo bar cat', ' ')
        sm4 = SelectorViewModel.generate_model('foo||bar|cat', '|')
        sm5 = SelectorViewModel.generate_model('foo::bar::cat')
        assert (sm1 == sm2 == sm3 == sm4 == sm5)

    def test_menu_view_model7(self):
        test_input = 'foo'
        expected_value = {'foo': {'': {}}}
        TestMenuViewModel.check_menu_model(test_input, expected_value)
