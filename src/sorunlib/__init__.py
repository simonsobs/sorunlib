from . import acu, seq, smurf

from .commands import wait
from .util import create_clients

CLIENTS = None


def initialize():
    global CLIENTS
    CLIENTS = create_clients()


__all__ = ["acu", "seq", "smurf", "wait", "initialize"]

from . import _version
__version__ = _version.get_versions()['version']
