from collections import UserDict
from datetime import datetime, timedelta
from fields import DATE_FORMAT

from record import Record

class AddressBook(UserDict):
  def __init__(self):
    super().__init__()
    self.last_id = 0

  def add_record(self, record: Record) -> None:
    self.last_id += 1
    self.data[self.last_id] = record

  def find(self, name: str) -> Record | None:
    record = next((record for record in self.data.values() if record.name.value == name), None)
    return record
  
  def delete(self, name: str):
    key = next((key for key in self.data.keys() if self.data[key].name.value == name), None)
    if not key:
       raise ValueError(f'record with name {name} not found in contacts')
    del self.data[key]

  def get_upcoming_birthdays(self):
    result = []
    
    current_date = datetime.today()
    current_year = current_date.year
    
    for record in self.data.values():
      if not record.birthday:
        continue
      
      birthdate = record.birthday.value.replace(current_year)
      if birthdate < current_date:
        birthdate = birthdate.replace(year=current_year + 1)

      if (birthdate - current_date).days > 7:
        continue
      
      congratulation_date = birthdate

      weekday = birthdate.weekday()
      if weekday == 5:
        congratulation_date = congratulation_date + timedelta(days=2)
      elif weekday == 6:
        congratulation_date = congratulation_date + timedelta(days=1)
      
      result.append({
        "name": record.name,
        "congratulation_date": datetime.strftime(congratulation_date, DATE_FORMAT) 
      })
    
    return result
