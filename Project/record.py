from datetime import datetime
from fields import Birthday, Name, Phone, Email, Address
from fields import DATE_FORMAT


class Record:
    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None
        self.address = None

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
        self.phones = [p for p in self.phones if p.value != phone]
        print(f'Phone {phone} successfully removed')

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        found_phone = self.find_phone(old_phone.strip())
        found_phone.value = new_phone
        print(f'New phone {new_phone} successfully replaced old phone {old_phone}')

    def find_phone(self, phone: str) -> Phone:
        phone = phone.strip()
        found_phone = next((p for p in self.phones if p.value == phone), None)
        if found_phone is None:
            raise ValueError(f'Phone {phone} not found in contacts')

        return found_phone

    def add_birthday(self, birthdate: str) -> None:
        self.birthday = Birthday(birthdate)

    def get_birthday(self) -> str:
        return (datetime.strftime(self.birthday.value, DATE_FORMAT)
                if self.birthday else None)

    def show_phones(self) -> str:
        return '; '.join(p.value for p in self.phones)

    def add_email(self, email: str) -> None:
        self.email = Email(email)

    def get_email(self) -> str:
        return self.email.value if self.email else None

    def add_address(self, address: str) -> None:
        address = address.strip()
        self.address = Address(address)

    def get_address(self) -> str:
        return self.address.value if self.address else None

    def __str__(self) -> str:
        return (f"Contact name: {self.name.value}, phones: {self.show_phones()}, "
                f"birthdate: {self.get_birthday() or 'not set'}, email: {self.get_email() or 'not set'}, "
                f"address: {self.get_address() or 'not set'}")
