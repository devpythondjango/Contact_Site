from django.core.exceptions import ValidationError
import re


def validate_passport_serial(serial):
    if not re.match(r'^[A-Z]{2}\d{7}$', serial):
        raise ValidationError('Pasport seriyasi noto\'g\'ri formatda')
    serial = serial.upper()
    first_letter = serial[0]
    if first_letter not in 'ABCD':
        raise ValidationError('Pasport seriyasining harfi noto\'g\'ri')
    return serial
