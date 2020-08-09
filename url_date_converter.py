"""
A Django custom path converter for handling ISO formatted dates.

url_date_converter -- path converter class for handling ISO formatted dates as Python 3 datetimes.
"""

from datetime import date

class url_date_converter:
    """
    A Django path converter for handling ISO formatted dates as Python 3 datetimes.
    """
    regex = '[0-9]{4}-[0-9]{2}-[0-9]{2}'

    def to_python(self, value):
        """Return the datetime from parsing value as an ISO date."""

        return date.fromisoformat(value)

    def to_url(self, value):
        """Return the string ISO representation of a datetime."""

        return value.isoformat()
