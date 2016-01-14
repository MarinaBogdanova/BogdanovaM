from lab4_5_6.project.models.fields.Field import Field
from lab4_5_6.project.models.fields.exceptions import FieldValidException

MAX_RANGE = int(10e9)


class IdField(Field):
    def __init__(self, id):
        self.set(id)

    def set(self, id):
        if not isinstance(id, int):
            raise FieldValidException("id must be int")
        if id not in range(1, MAX_RANGE):
            raise FieldValidException("id should be range from 1 to " + str(MAX_RANGE))
        self._id = id

    def get(self):
        # if not hasattr(self, '_id'):
        #     raise FieldUndefinedException
        return self._id