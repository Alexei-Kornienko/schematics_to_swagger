import inspect
from collections import namedtuple

from schematics import models
from schematics import types

name = 'schematics_to_swagger'

DEFAULT_SWAGGER_VERSION = 2

SwaggerProp = namedtuple('SwaggerProp', ['name', 'func'], defaults=(None, lambda x: x))

_KNOWN_PROPS = {
    'max_length': SwaggerProp('maxLength'),
    'min_length': SwaggerProp('minLength'),
    'regex': SwaggerProp('pattern', lambda x: x.pattern),
    'choices': SwaggerProp('enum'),
}


def _map_type_properties(t):
    props = {}
    for k, v in _KNOWN_PROPS.items():
        prop_value = getattr(t, k, None)
        if prop_value:
            props[v.name] = v.func(prop_value)
    # passthrough metadata items
    for k, v in t.metadata.items():
        props[k] = v
    return props


_DATATYPES = {
    # Base types
    types.BooleanType: lambda t: dict(type='boolean', **_map_type_properties(t)),
    types.IntType: lambda t: dict(type='integer', format='int32', **_map_type_properties(t)),
    types.LongType: lambda t: dict(type='integer', format='int64', **_map_type_properties(t)),
    types.FloatType: lambda t: dict(type='number', format='float', **_map_type_properties(t)),
    types.DecimalType: lambda t: dict(type='number', format='double', **_map_type_properties(t)),
    types.StringType: lambda t: dict(type='string', **_map_type_properties(t)),
    types.UUIDType: lambda t: dict(type='string', format='uuid', **_map_type_properties(t)),
    types.MD5Type: lambda t: dict(type='string', format='md5', **_map_type_properties(t)),
    types.SHA1Type: lambda t: dict(type='string', format='sha1', **_map_type_properties(t)),
    types.DateType: lambda t: dict(type='string', format='date', **_map_type_properties(t)),
    types.DateTimeType: lambda t: dict(type='string', format='date-time', **_map_type_properties(t)),

    # Net types
    types.EmailType: lambda t: dict(type='string', format='email', **_map_type_properties(t)),
    types.URLType: lambda t: dict(type='string', format='uri', **_map_type_properties(t)),

    # Compound types
    types.ModelType: lambda t: dict({'$ref': '#/definitions/%s' % t.model_name}, **_map_type_properties(t)),
    types.ListType: lambda t: dict(type='array', items=_map_schematics_type(t.field), **_map_type_properties(t))
}


def _map_schematics_type(t):
    if t.__class__ in _DATATYPES:
        return _DATATYPES[t.__class__](t)


def model_to_definition(model):
    properties = {}
    required = []

    for field_name, field in model.fields.items():
        if field_name.startswith(f'_{model.__name__}'):
            continue  # Exclude private fields
        properties[field_name] = _map_schematics_type(field)
        if getattr(field, 'required'):
            required.append(field_name)

    result_info = {
        'type': 'object',
        'title': model.__name__,
        'description': model.__doc__,
        'properties': properties
    }
    if required:
        result_info['required'] = required
    return result_info


def version_dependencies(version):
    if version == 3:
        global _DATATYPES
        _DATATYPES.update({
            types.ModelType: lambda t: dict(
                {'$ref': '#/components/schemas/%s' % t.model_name}, **_map_type_properties(t)
            )
        })


def read_models_from_module(module, version=DEFAULT_SWAGGER_VERSION):
    version_dependencies(version)
    results = {}
    for item in dir(module):
        if item.startswith('_'):
            continue  # Skip private stuff
        obj = getattr(module, item)
        if inspect.isclass(obj) and issubclass(obj, models.Model) and obj.__module__ == module.__name__:
            results[item] = model_to_definition(obj)
    return results
