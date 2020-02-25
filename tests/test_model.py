import schematics_to_swagger

from tests import models


WEATHER_REPORT_DEFINITION = {
    'title': 'WeatherReport',
    'type': 'object',
    'description': 'Some sample class for Weather report',
    'properties': {
        'city': {
            'type': 'string',
            'maxLength': 50,
            'readOnly': True
        },
        'temperature': {
            'type': 'number',
            'format': 'double'
        },
        'author': {
            'type': 'string',
            'format': 'email',
        },
        'some_url': {
            'type': 'string',
            'format': 'uri',
        },
        'taken_at': {
            'type': 'string',
            'format': 'date-time'
        }
    },
    'required': ['temperature']
}
WEATHER_STATS_DEF = {
    'title': 'WeatherStats',
    'type': 'object',
    'description': None,
    'properties': {
        'last_report': {'$ref': '#/definitions/WeatherReport'},
        'prev_reports': {
            'type': 'array',
            'items': {
                '$ref': '#/definitions/WeatherReport'
            }
        },
        'date_list': {
            'type': 'array',
            'items': {
                'type': 'string',
                'format': 'date-time'
            }
        }
    },
}
WEATHER_STATS_DEF_V3 = {
    'title': 'WeatherStats',
    'type': 'object',
    'description': None,
    'properties': {
        'last_report': {
            '$ref': '#/components/schemas/WeatherReport'
        },
        'prev_reports': {
            'type': 'array',
            'items': {
                '$ref': '#/components/schemas/WeatherReport'
            },
        },
        'date_list': {
            'type': 'array',
            'items': {
                'type': 'string',
                'format': 'date-time'
            }
        }
    },
}
WEATHER_PRIVATE_DATA = {
    'title': 'WeatherPrivateData',
    'type': 'object',
    'description': 'Some sample model with private field',
    'properties': {
        'city': {
            'type': 'string',
            'maxLength': 50,
            'readOnly': True
        },
        'temperature': {
            'type': 'number',
            'format': 'double',
            'minimum': -50,
            'maximum': 50
        }
    },
    'required': ['temperature']
}


def test_model_to_definition():
    expected = WEATHER_REPORT_DEFINITION
    definition = schematics_to_swagger.model_to_definition(models.WeatherReport)
    assert expected == definition


def test_read_models_from_module():
    expected = {
        'WeatherReport': WEATHER_REPORT_DEFINITION,
        'WeatherStats': WEATHER_STATS_DEF,
        'WeatherPrivateData': WEATHER_PRIVATE_DATA
    }
    data = schematics_to_swagger.read_models_from_module(models)
    assert expected == data


def test_compound_type():
    expected = WEATHER_STATS_DEF
    data = schematics_to_swagger.model_to_definition(models.WeatherStats)
    assert expected == data


def test_private_fields():
    expected = WEATHER_PRIVATE_DATA
    definition = schematics_to_swagger.model_to_definition(models.WeatherPrivateData)
    assert expected == definition


def test_read_models_from_module_v3():
    expected = {
        'WeatherReport': WEATHER_REPORT_DEFINITION,
        'WeatherStats': WEATHER_STATS_DEF_V3,
        'WeatherPrivateData': WEATHER_PRIVATE_DATA
    }
    data = schematics_to_swagger.read_models_from_module(models, version=3)
    assert expected == data