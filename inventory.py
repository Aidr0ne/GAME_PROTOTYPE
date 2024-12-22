import settings as s

_inventory = []

def set(items):
    global _inventory
    _inventory = items
    return _inventory

def get():
    return _inventory