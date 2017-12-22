"""
Logging subsystem of aigym system.

logger - general logger object for across-system use.
"""
from .mixins import LoggerMixin

logger = LoggerMixin().logger
