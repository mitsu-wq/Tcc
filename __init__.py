"""
Package initialization for the TCC (Tactical Control Component) module.

Exports the main Tcc class and TccState enumeration for external use.
"""
import os
import logging
from .TccCan import TccCan
from .TccTypes import TccState, TccCommand, TccParameter, TccTimeout
from json import load

try:
    config_path = os.path.join(os.path.dirname(__file__), 'logging.json')
    with open(config_path, 'r') as f:
        logging.config.dictConfig(load(f))
except FileNotFoundError:
    logging.basicConfig(level=logging.WARNING)
    logging.getLogger(__name__).warning("logging.json not found, using default logging")

__all__ = ["TccCan", "TccState", "TccCommand", "TccParameter", "TccTimeout"]