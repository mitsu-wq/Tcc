"""
Logger package for TCC server.

Provides a configurable logging utility for the project.
"""

from .logger import setup_logger
import logging

# Создаем логгер по умолчанию
default_logger = setup_logger("tcc_server", log_file="tcc_server.log", level=logging.INFO)

__all__ = ["setup_logger", "default_logger"]