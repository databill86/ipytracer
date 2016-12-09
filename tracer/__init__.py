# -*- coding: UTF-8 -*-

"""
    tracer
    ~~~~~~

    Algorithm visualizer for Jupyter/IPython Notebook
"""


from .tracer import *


__author__ = 'Han Lee (@sn0wle0pard)'
__version__ = '0.0.1'
__copyright__ = 'Copyright (c) 2016 Han Lee'
__license__ = 'MIT'


def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'static',
        'dest': 'tracer',
        'require': 'tracer/extension'
    }]


def _jupyter_labextension_paths():
    return [{
        'name': 'tracer',
        'src': 'staticlab',
    }]