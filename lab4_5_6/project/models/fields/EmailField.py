import re

from lab4_5_6.project.models.fields.Field import Field
from lab4_5_6.project.models.fields.exceptions import FieldValidException

NAME_MIN_LENGTH = 1
NAME_MAX_LENGTH = 128

DOMAIN_MIN_LENGTH = 4
DOMAIN_MAX_LENGTH = 256


class EmailField(Field):
    def __init__(self, email):
        self.set(email)

    def set(self, email):
        if not isinstance(email, str):
            raise FieldValidException("email must be string")
        if not re.search(r'[\w.-]+@[\w.-]+.\w+', email):
            raise FieldValidException("email must have the form: name@domain.zone")
        name, domain = email.split('@')
        if len(name) not in range(NAME_MIN_LENGTH, NAME_MAX_LENGTH):
            raise FieldValidException(
                "length email name should be from " + str(NAME_MIN_LENGTH) + " to " + str(NAME_MAX_LENGTH))
        if len(domain) not in range(DOMAIN_MIN_LENGTH, DOMAIN_MAX_LENGTH):
            raise FieldValidException(
                "length email name should be from " + str(DOMAIN_MIN_LENGTH) + " to " + str(DOMAIN_MAX_LENGTH))
        self._name = name
        self._domain = domain

    def get(self):
        # if not hasattr(self, '_name') or not hasattr(self, '_domain'):
        #     raise FieldUndefinedException
        return self._name + "@" + self._domain