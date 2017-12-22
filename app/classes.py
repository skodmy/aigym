"""
This module defines base application classes for client applications.

On the top of hierarchy lives class AIApplication which defines common interface for all applications.
This interface also forms application lifecycle.
Application lifecycle consists from 3 main parts:
    1.Creation(Initialization).
    2.Running.
    3.Closing(Finalization).
First step is defined by AIApplication instance __init__(self) method.
Second -- run(self) method.
Third -- close(self) method.

"""
from typing import Any


class AIApplication:
    """
    Application base class.

    Stays on top of the hierarchy and defines application lifecycle.
    """
    def __init__(self):
        """
        Application initialization goes here.
        """
        pass

    def __del__(self):
        """
        Runs self.close() to finalize self.
        """
        self.close()

    def run(self):
        """
        Application logic goes here.
        """
        pass

    def close(self):
        """
        Application finalization goes here.
        """
        pass


class BackendedAIApplication(AIApplication):
    """
    Base class for apps that are using some backend.
    """
    def __init__(self, backend=None):
        super().__init__()
        self._backend = backend

    @property
    def backend(self) -> Any:
        return self._backend

    @backend.setter
    def backend(self, obj: Any):
        if obj is not None:
            self._backend = obj
