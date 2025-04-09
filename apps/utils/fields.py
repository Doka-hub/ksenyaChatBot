import os
from pathlib import Path

import peewee


# TODO: test it
class FileField(peewee.CharField):
    def __init__(self, upload_to='', *args, **kwargs):
        kwargs['null'] = True
        kwargs['max_length'] = 255
        self.upload_to = upload_to
        super().__init__(*args, **kwargs)

    def db_value(self, value):
        return value.name if value else None

    def python_value(self, value):
        return Path(value) if value else None

    def save_file(self, instance, filepath):
        filepath = Path('media/', self.upload_to) / filepath
        setattr(instance, self.name, filepath)
        return filepath

    def delete_file(self, instance):
        filepath = getattr(instance, self.name)
        if filepath and os.path.exists(filepath):
            os.remove(filepath)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return getattr(instance, self.name)

    def __set__(self, instance, value):
        if isinstance(value, (bytes, bytearray)):
            filename = value
            self.save_file(instance, filename, value)
        elif isinstance(value, str):
            filename = Path(value).name
            self.save_file(instance, filename, value.encode())
        elif value is None:
            self.delete_file(instance)
        else:
            raise TypeError(f"{self.name} must be bytes, bytearray or str")
