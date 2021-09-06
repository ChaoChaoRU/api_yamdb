import datetime

from django.core.exceptions import ValidationError


def year_validator(year):
    current_year = datetime.date.today().year
    if year > current_year:
        raise ValidationError(
            'The year of publishing can not be bigger than current year'
        )
