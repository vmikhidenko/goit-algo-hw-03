from datetime import datetime
import re

DATE_FORMAT = "%d.%m.%Y"
ADDRESS_MAX_LENGTH = 80
PHONE_LENGTH = 10


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value: str):
        if not value.isdigit() or len(value) != PHONE_LENGTH:
            raise ValueError(f"Phone must be a number of length {PHONE_LENGTH}")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value: str) -> None:
        try:
            self.value = datetime.strptime(value, DATE_FORMAT)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Email(Field):

    EMAIL_PATTERN = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    def __init__(self, value: str) -> None:
        if not re.match(self.EMAIL_PATTERN, value):
            raise ValueError("Invalid email address")
        super().__init__(value)


class Address(Field):
    def __init__(self, value: str) -> None:
        if len(value) > ADDRESS_MAX_LENGTH:
            raise ValueError(
                f"Address should be {ADDRESS_MAX_LENGTH} characters or less"
            )
        super().__init__(value)
