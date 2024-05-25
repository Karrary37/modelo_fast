import ast

from config import settings


def define_routing_key(routing_key):
    list_routing_keys = ast.literal_eval(settings.ROUTING_KEYS)
    if routing_key not in list_routing_keys:
        routing_key = 'precessao'
    return routing_key


def verify_routing_key(routing_key):
    list_routing_keys = ast.literal_eval(settings.ROUTING_KEYS)
    if routing_key not in list_routing_keys:
        return False
    return True
