import datetime
from schematics.models import Model
from schematics import types


class WeatherReport(Model):
    """Some sample class for Weather report"""
    city = types.StringType(max_length=50, metadata={'readOnly': True})
    temperature = types.DecimalType(required=True)
    taken_at = types.DateTimeType(default=datetime.datetime.now)
    author = types.EmailType()
    some_url = types.URLType()


class WeatherStats(Model):
    last_report = types.ModelType(WeatherReport)
    prev_reports = types.ListType(types.ModelType(WeatherReport))
    date_list = types.ListType(types.DateTimeType())
