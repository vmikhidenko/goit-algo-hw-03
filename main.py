from datetime import datetime

from address_book import AddressBook
from record import Record
from fields import DATE_FORMAT
from data_saver import data_saver
from notebook import add_note_command, add_tags_command, edit_note_command, delete_note_command, find_note_by_tag_command, find_note_command, remove_tag_command, show_all_notes_command, sort_notes_by_tag_command
from decorators import input_error

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

@input_error
def add_email(args, book: AddressBook):
  name, email = args
  if not name or not email:
    raise ValueError('You need to specify name and email')

  existing_contact = book.find(name)
  if not existing_contact:
    return f'There is no contact with name {name}'
  
  existing_contact.add_email(email)
  return f'email {email} successfully added to contact {name}'

@input_error
def add_address(args, book: AddressBook):
  name, address = args
  if not name or not address:
    raise ValueError('You need to specify name and address')

  existing_contact = book.find(name)
  if not existing_contact:
    return f'There is no contact with name {name}'
  
  existing_contact.add_address(address)
  return f'address {address} successfully added to contact {name}'

def main():
  print("Welcome to the assistant bot!")
  book = data_saver.load_data()
  notebook = data_saver.load_notebook()
  
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

  # print('Add new note')
  # args = 'note one', "this is the text of the note"
  # print(add_note_command(args, notebook))
  # print()

  # print('Add note that already exists')
  # args = 'note one', "this is the text of the note"
  # print(add_note_command(args, notebook))
  # print()

  # print('Edit note that exists')
  # args = 'note one', "this is edited text for note one"
  # print(edit_note_command(args, notebook))
  # print()
  
  # print('Edit note that does not exist')
  # args = 'note two', "this is edited text for note two"
  # print(edit_note_command(args, notebook))
  # print()

  # print('Delete note that exists')
  # args = 'note one',
  # print(delete_note_command(args, notebook))
  # print()

  # print('Delete note that does not exist')
  # args = 'note two',
  # print(delete_note_command(args, notebook))
  # print()
  
  # print('Find note by text which exists')
  # args = 'note one', "this is the text of the note"
  # print(add_note_command(args, notebook))
  # args = 'note two', "apchhui"
  # print(add_note_command(args, notebook))
  # args = 'note three', "this is sss"
  # print(add_note_command(args, notebook))
  # args = 'this iS',
  # print(find_note_command(args, notebook))
  # print()

  # print('Find note by text which does not exist')
  # args = 'asdfsdf',
  # print(find_note_command(args, notebook))
  # print()

  # print('Show all notes')
  # print(show_all_notes_command(notebook))

  while True:
    user_input = input("Enter a command: ").strip()
    command, *args = parse_input(user_input)

    if command in ["close", "exit"]:
      data_saver.save_data(book)
      data_saver.save_notebook(notebook)
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
    elif command == 'add-note':
      print(add_note_command(args, notebook))
    elif command == 'edit-note':
      print(edit_note_command(args, notebook))
    elif command == 'delete-note':
      print(delete_note_command(args, notebook))
    elif command == 'find-note':
      print(find_note_command(args, notebook))
    elif command == 'show-all-notes':
      print(show_all_notes_command(notebook))
    elif command == "add-email":
      print(add_email(args, book))
    elif command == "add-address":
      print(add_address(args, book))
    elif command == 'add-tags':
      print(add_tags_command(args, notebook))
    elif command == 'sort-notes-by-tag':
      print(sort_notes_by_tag_command(args, notebook))
    elif command == 'find-note-by-tag':
        print(find_note_by_tag_command(args, notebook))
    elif command == 'remove-tag':
      print(remove_tag_command(args, notebook))
    else:
      print("Invalid command.")

      
if __name__ == '__main__':
  main()

