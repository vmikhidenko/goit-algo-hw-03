from datetime import datetime

DATE_FORMAT = "%d.%m.%Y"
EMAIL_MAX_LENGTH=30
ADDRESS_MAX_LENGTH=80
PHONE_LENGTH=10

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
      raise ValueError(f'Phone must be a number of length {PHONE_LENGTH}') 
    super().__init__(value)


class Birthday(Field):
  def __init__(self, value: str) -> None:
    try:
      self.value = datetime.strptime(value, DATE_FORMAT)
    except ValueError:
      raise ValueError("Invalid date format. Use DD.MM.YYYY")
    
class Email(Field):
  def __init__(self, value: str) -> None:
    if '@' not in value:
      raise ValueError(f'Invalid email address')
    if len(value) > EMAIL_MAX_LENGTH:
      raise ValueError(f'Email should be {EMAIL_MAX_LENGTH} characters or less')
    super().__init__(value)

class Address(Field):
  def __init__(self, value: str) -> None:
    if len(value) > ADDRESS_MAX_LENGTH:
      raise ValueError(f'Address should be {ADDRESS_MAX_LENGTH} characters or less')
    super().__init__(value)
