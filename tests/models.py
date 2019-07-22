import datetime
from schematics.models import Model
from schematics.types import StringType, DecimalType, DateTimeType


class WeatherReport(Model):
    """Some sample class for Weather report"""
    city = StringType(max_length=50)
    temperature = DecimalType(required=True)
    taken_at = DateTimeType(default=datetime.datetime.now)
