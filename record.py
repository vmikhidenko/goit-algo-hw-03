from datetime import datetime
from fields import Birthday, Name, Phone
from fields import DATE_FORMAT

class Record:
  def __init__(self, name: str) -> None:
    self.name = Name(name)
    self.phones = []
    self.birthday = None

  def add_phone(self, phone: str) -> None:
    phone = phone.strip()
    found = False
    try:
      self.find_phone(phone)
      found = True  
    except:
      pass

    if found:
       raise ValueError(f'Phone {phone} already exists in contacts')
    
    self.phones.append(Phone(phone))

  def remove_phone(self, phone: str) -> None:
    phone = phone.strip()
    self.phones = list(filter(lambda p: p['value'] == phone, self.phones))
    print(f'Phone {phone} successfully removed')
  
  def edit_phone(self, old_phone: str, new_phone: str) -> None:
    found_phone = self.find_phone(old_phone.strip())
    found_phone.value = new_phone
    print(f'New phone {new_phone} successfully replaced old phone {old_phone}')
  
  def find_phone(self, phone: str) -> str:
    phone = phone.strip()
    
    found_phone = next((p for p in self.phones if p.value == phone), None)
    if found_phone == None:
      raise Exception(f'Phone {phone} not found in contacts')
    
    return found_phone

  def add_birthday(self, birthdate: str) -> None:
    self.birthday = Birthday(birthdate)
    
  def get_birthday(self):
    return datetime.strftime(self.birthday.value, DATE_FORMAT) if self.birthday else None

  def show_phones(self) -> str:
    return '; '.join(p.value for p in self.phones)

  def __str__(self):
    return f"Contact name: {self.name.value}, phones: {self.show_phones()}, birthdate: {self.get_birthday() or  'not set'}"
  
