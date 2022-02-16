from .util import create_clients

CLIENTS = None

def init_clients():
    global CLIENTS
    CLIENTS = create_clients()
