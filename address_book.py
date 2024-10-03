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
        return next(
            (record for record in self.data.values() if record.name.value == name), 
            None
        )

    def delete(self, name: str) -> None:
        key = next(
            (key for key in self.data.keys() if self.data[key].name.value == name), 
            None
        )
        if not key:
            raise ValueError(f'Record with name {name} not found in contacts')
        del self.data[key]

    def add_birthday(self, name: str, birthday_str: str) -> None:
        record = self.find(name)
        if record is None:
            raise ValueError(f'Record with name {name} not found in contacts')
        
        try:
            birthday = datetime.strptime(birthday_str, DATE_FORMAT)
        except ValueError:
            raise ValueError(f'Invalid date format. Please use {DATE_FORMAT}')
        
        record.birthday = birthday
        print(f'Birthday for {name} set to {birthday.strftime(DATE_FORMAT)}')


    def get_upcoming_birthdays(self) -> list[dict]:
        result = []
        current_date = datetime.today()
        current_year = current_date.year

        for record in self.data.values():
            if not record.birthday:
                continue
            
            birthdate = record.birthday.value.replace(year=current_year)
            if birthdate < current_date:
                birthdate = birthdate.replace(year=current_year + 1)

            if (birthdate - current_date).days > 7:
                continue

            congratulation_date = birthdate
            weekday = birthdate.weekday()
            if weekday == 5:
                congratulation_date += timedelta(days=2)
            elif weekday == 6:
                congratulation_date += timedelta(days=1)

            result.append({
                "name": record.name.value,
                "congratulation_date": datetime.strftime(congratulation_date, DATE_FORMAT)
            })

        return result
