from lab4_5_6.project.models.fields.Field import Field
from lab4_5_6.project.models.fields.exceptions import FieldValidException

MESSAGE_MIN_LENGTH = 0
MESSAGE_MAX_LENGTH = 10000


class MessageField(Field):
    def __init__(self, message):
        self.set(message)

    def set(self, message):
        if not isinstance(message, str):
            raise FieldValidException("message must be string")
        if len(message) not in range(MESSAGE_MIN_LENGTH, MESSAGE_MAX_LENGTH):
            raise FieldValidException(
                "length theme should be from " + str(MESSAGE_MIN_LENGTH) + " to " + str(MESSAGE_MAX_LENGTH))
        self._message = message

    def get(self):
        return self._message