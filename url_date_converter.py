from datetime import date

class url_date_converter:
    regex = '[0-9]{4}-[0-9]{2}-[0-9]{2}'

    def to_python(self, value):

        return date.fromisoformat(value)

    def to_url(self, value):

        return value.isoformat()
