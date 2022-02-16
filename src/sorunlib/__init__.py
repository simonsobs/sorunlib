from .util import create_clients

__all__ = ["acu", "seq", "smurf"]

CLIENTS = None

def init_clients():
    global CLIENTS
    CLIENTS = create_clients()
