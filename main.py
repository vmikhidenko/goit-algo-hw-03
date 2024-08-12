from datetime import datetime

from address_book import AddressBook
from record import Record
from fields import DATE_FORMAT
from data_saver import data_saver


def input_error(func):
  def inner(*args, **kwargs):
    try:
      return func(*args, **kwargs)
    except ValueError as ve:
      return f"Error happened: {ve}"
    except KeyError:
      return "Contact does no exist"
    except IndexError as e:
      return f"I have no idea where this error can occur in the existing code, but here is the error: {e}"

  return inner

@input_error
def add_birthday(args, book: AddressBook):
  name, birthdate = args
  if not name or not birthdate:
    raise ValueError('You need to specify name and birthdate')

  existing_contact = book.find(name)
  if not existing_contact:
    return f'There is no contact with name {name}'
  
  existing_contact.add_birthday(birthdate)
  return f'birthday {birthdate} successfully added to contact {name}'


@input_error
def show_birthday(args, book):
  name, *_ = args
  if not name:
    raise ValueError('You need to specify name')

  existing_contact = book.find(name)
  if not existing_contact:
    return f'There is no contact with name {name}'
  
  birthdate = existing_contact.get_birthday()
  if not birthdate:
    return f"{name}'s birthdate is not set"

  birthdate = datetime.strftime(existing_contact.get_birthday(), DATE_FORMAT)
  return f"{name}'s birthday is {birthdate}"

@input_error
def birthdays(book: AddressBook):
  upcoming_birthdays = book.get_upcoming_birthdays()
  if len(upcoming_birthdays) == 0:
    return 'No contacts with upcoming birthdays'
  
  result_strings = []
  for item in upcoming_birthdays:
    result_strings.append(f'name {item.get('name')}, congratulation date: {item.get('congratulation_date')}')
  
  return '\n'.join(result_strings)

def parse_input(user_input: str):
  cmd, *args = user_input.split()
  cmd = cmd.strip().lower()
  return cmd, *args

@input_error
def add_contact(args, book: AddressBook) -> None:
  name, phone, *_ = args
  record = book.find(name)
  
  if record is None:
      record = Record(name)
      book.add_record(record)
      message = "Contact added."
  if phone:
      record.add_phone(phone)
      message = "Contact updated."
  return message

@input_error
def change_contact(args, book: AddressBook):
  name, old_phone, new_phone = args
  if not name or not old_phone or not new_phone:
    raise ValueError('To change contact specify: <name>, <old_phone>, <new_phone>')

  existing_contact = book.find(name)
  if not existing_contact:
    return f"contact with name {name} does not exist"
  
  existing_contact.edit_phone(old_phone, new_phone)
  return f"Old phone {old_phone} was replaced by new phone {new_phone} for contact {existing_contact.name}."

@input_error
def show_phone(args, book: AddressBook):
  name, *_ = args
  if not name:
    raise ValueError('Please enter contact name')
  
  contact = book.find(name)
  if not contact:
    return f'There is not contact with name {name}'
  
  return contact.show_phones()

def show_all(book: AddressBook):
  if not book.data.keys():
    return "There is no contacts in the list"
  
  result = []
  for contact in book.data.values():
    result.append(f"{contact}")
  return "\n".join(result)





def main():
  print("Welcome to the assistant bot!")
  book = data_saver.load_data()
  
  # testing
  # print('Add contact')
  # args = 'Vasya', '1234567890'
  # print(add_contact(args, book))
  # print(show_all(book))
  # print()
  
  # print('Update contact if there is such already')
  # args = 'Vasya', '0987654321'
  # print(add_contact(args, book))
  # print(show_all(book))
  # print()

  # print('Update contact if there is such already')
  # args = 'Vasya', '0987654321', '1111111111'
  # print(change_contact(args, book))
  # print(show_all(book))
  # print()

  # print('Update contact if there is no such contact')
  # args = 'Vasy', '0987654321', '1111111111'
  # print(change_contact(args, book))
  # print(show_all(book))
  # print()

  # print('Show existing contact')
  # args = 'Vasya',
  # print(show_phone(args, book))
  # print(show_all(book))
  # print()

  # print('Show non existing contact')
  # args = 'Vasy',
  # print(show_phone(args, book))
  # print(show_all(book))
  # print()

  # print('Add birthdate to existing contact')
  # args = 'Vasya', '01.01.2023'
  # print(add_birthday(args, book))
  # print(show_all(book))
  # print()

  # print('Add birthdate to existing contact in incoorect format')
  # vasyas_birthdate = date.today() + timedelta(days=2)
  # args = 'Vasya', datetime.strftime(vasyas_birthdate, DATE_FORMAT)
  # print(add_birthday(args, book))
  # print(show_all(book))
  # print()

  # print('Add birthdate to non existing contact')
  # args = 'Vasy', '01.01.2021'
  # print(add_birthday(args, book))
  # print(show_all(book))
  # print()

  # print('Show birthdate of existing contact')
  # args = 'Vasya',
  # print(show_birthday(args, book))
  # print(show_all(book))
  # print()

  # print('Show birthdate of non existing contact')
  # args = 'Vasy',
  # print(show_birthday(args, book))
  # print(show_all(book))
  # print()

  # print('Show birthdate of it is not set for the contact')
  # args = 'Petya', '0987654321'
  # print(add_contact(args, book))
  # args = 'Petya',
  # print(show_birthday(args, book))
  # print(show_all(book))
  # print()
  
  # print('Show future birthday guys')
  # print(birthdays(book))

  while True:
    user_input = input().strip()
    command, *args = parse_input(user_input)

    if command in ["close", "exit"]:
      data_saver.save_data(book)
      print("Good bye!")
      break
    elif command == 'hello':
      print('How can I help you?')
    elif command == 'add':
      print(add_contact(args, book))
    elif command == 'change':
      print(change_contact(args, book))
    elif command == 'phone':
      print(show_phone(args, book))
    elif command == 'all':
      print(show_all(book))
    elif command == "add-birthday":
      print(add_birthday(args, book))
    elif command == "show-birthday":
      print(show_birthday(args, book))
    elif command == "birthdays":
      print(birthdays(book))
    else:
      print("Invalid command.")

      
if __name__ == '__main__':
  main()

