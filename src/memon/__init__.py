# -*- coding: utf-8 -*-
from .memon import MemoryMonitor
import pkg_resources

try:
    __version__ = pkg_resources.get_distribution(__name__).version
except:
    __version__ = 'unknown'
