"""
This module is is interpreted when something from app or itself package is imported.

There base application classes are imported from classes module to make import in client code more short.
For example, you will have to write next code:

from aigym.app import Application

class YourApp(Application):
    pass

__all__ tuple defines items that can be imported from aigym.app package.
"""
from .classes import AIApplication, BackendedAIApplication

__all__ = ('AIApplication', 'BackendedAIApplication')
