from . import acu, seq, smurf

from .commands import wait
from .util import create_clients

CLIENTS = None


def initialize():
    global CLIENTS
    CLIENTS = create_clients()


__all__ = ["acu", "seq", "smurf", "wait", "initialize"]
