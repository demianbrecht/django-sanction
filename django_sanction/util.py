from importlib import import_module

def import_string(path):
    mname, cname = path.rsplit('.', 1)
    return getattr(import_module(mname), cname)
