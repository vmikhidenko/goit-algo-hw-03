from datetime import datetime

DATE_FORMAT = "%d.%m.%Y"

class Field:
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return str(self.value)

class Name(Field):
  pass

class Phone(Field):
  def __init__(self, value: str):
    if not value.isdigit() or len(value) != 10:
      raise ValueError(f'Phone must be a number of length 10') 
    super().__init__(value)


class Birthday(Field):
  def __init__(self, value: str) -> None:
    try:
      self.value = datetime.strptime(value, DATE_FORMAT)
    except ValueError:
      raise ValueError("Invalid date format. Use DD.MM.YYYY")
