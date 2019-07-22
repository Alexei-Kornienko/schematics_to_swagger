import inspect
from schematics import models
from schematics import types

_KNOWN_PROPS = {
    'required': 'required',
    'max_length': 'maxLength',
    'min_length': 'minLength',
    'regex': 'pattern'
}


def _map_type_properties(t):
    props = {}
    for k, v in _KNOWN_PROPS.items():
        prop_value = getattr(t, k, None)
        if prop_value:
            props[v] = prop_value
    return props


_DATATYPES = {
    types.StringType: lambda t: dict(type='string', **_map_type_properties(t)),
    types.DecimalType: lambda t: dict(type='number', **_map_type_properties(t)),
    types.DateTimeType: lambda t: dict(type='string', format='date-time', **_map_type_properties(t))
}


def _map_schematics_type(t):
    if t.__class__ in _DATATYPES:
        return _DATATYPES[t.__class__](t)


def model_to_definition(model):
    return {
        'type': 'object',
        'title': model.__name__,
        'description': model.__doc__,
        'properties': {k: _map_schematics_type(v) for k, v in model._fields.items()}
    }


def read_models_from_module(module):
    results = {}
    for item in dir(module):
        if item.startswith('_'):
            continue  # Skip private stuff
        obj = getattr(module, item)
        if inspect.isclass(obj) and issubclass(obj, models.Model) and obj.__module__ == module.__name__:
            results[item] = model_to_definition(obj)
    return results
