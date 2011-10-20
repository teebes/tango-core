"Templating hooks for injecting context into stash (and app) templates."

GLOBAL_CONTEXT_MARKER = '_tango_global_context'
CONTEXT_PROCESSOR_MARKER = '_tango_context_processor'
MARKER = object()


def global_context(obj):
    "Mark function or object for injection into app's global template context."
    setattr(obj, GLOBAL_CONTEXT_MARKER, MARKER)
    return obj


def context_processor(function):
    "Mark function for registration as a global template context processor."
    setattr(function, CONTEXT_PROCESSOR_MARKER, MARKER)
    return function


def get_global_context(module):
    "Get a dict of all marked global context variables."
    global_context = {}
    for name in vars(module):
        attr = getattr(module, name)
        if getattr(attr, GLOBAL_CONTEXT_MARKER, None) is MARKER:
            global_context[name] = attr
    return global_context


def get_context_processors(module):
    "Get a list of all marked context processors in a module."
    context_processors = []
    for name in vars(module):
        attr = getattr(module, name)
        if getattr(attr, CONTEXT_PROCESSOR_MARKER, None) is MARKER:
            context_processors.append(attr)
    return context_processors
