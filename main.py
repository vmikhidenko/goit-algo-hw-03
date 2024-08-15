from datetime import datetime
from address_book import AddressBook
from notebook import Notebook
from record import Record
from fields import DATE_FORMAT
from data_manager import DataManager
import constants as const
from notebook import (
    add_note_command, add_tags_command, edit_note_command, delete_note_command, 
    find_note_by_tag_command, find_note_command, remove_tag_command, show_all_notes_command, 
    sort_notes_by_tag_command
)
from decorators import input_error
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

# Define commands for autocompletion
commands = [
    'add', 'change', 'phone', 'all', 'add-birthday', 'show-birthday', 'birthdays', 
    'hello', 'close', 'exit', 'help', 'remove', 'add-note', 'edit-note', 'delete-note', 
    'find-note', 'show-all-notes', 'add-email', 'add-address', 'add-tags', 
    'sort-notes-by-tag', 'find-note-by-tag', 'remove-tag', 'search'
]

# Create a WordCompleter for command autocompletion
command_completer = WordCompleter(commands, ignore_case=True)

data_manager = DataManager()
data_manager.add_storage(const.ADDRESS_BOOK_STORAGE_ID, const.ADDRESS_BOOK_FILE, AddressBook)
data_manager.add_storage(const.NOTEBOOK_STORAGE_ID, const.NOTEBOOK_FILE, Notebook)

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
def show_birthday(args, book: AddressBook):
    name, *_ = args
    if not name:
        raise ValueError('You need to specify name')

    existing_contact = book.find(name)
    if not existing_contact:
        return f'There is no contact with name {name}'
    
    birthdate = existing_contact.get_birthday()
    if not birthdate:
        return f"{name}'s birthdate is not set"

    if isinstance(birthdate, str):
        try:
            birthdate = datetime.strptime(birthdate, DATE_FORMAT)
        except ValueError:
            return f"Error: Birthday date format is incorrect for {name}"

    birthdate_str = birthdate.strftime(DATE_FORMAT)
    return f"{name}'s birthday is {birthdate_str}"

@input_error
def birthdays(book: AddressBook):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if len(upcoming_birthdays) == 0:
        return 'No contacts with upcoming birthdays'
    
    result_strings = []
    for item in upcoming_birthdays:
        result_strings.append(f'name {item.get("name")}, congratulation date: {item.get("congratulation_date")}')
    
    return '\n'.join(result_strings)

def parse_input(user_input: str):
    command, *args = user_input.split()
    command = command.strip().lower()
    return command, *args

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
def delete_contact(args, book: AddressBook):
    name, *_ = args
    if not name:
        raise ValueError('To delete contact specify: <name>')

    existing_contact = book.find(name)
    if not existing_contact:
        return f"Contact with name \"{name}\" does not exist"

    book.delete(name)
    return f"Contact with name \"{name}\" successfully deleted"

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
    if len(args) < 2:
        raise ValueError('You need to specify name and address')
    name = args[0]
    address = ' '.join(args[1:]).strip()

    existing_contact = book.find(name)
    if not existing_contact:
        return f'There is no contact with name {name}'
    
    existing_contact.add_address(address)
    return f'Address {address} successfully added to contact {name}'

@input_error
def search_contact(args, book: AddressBook):
    search, *_ = args
    if not search:
        raise ValueError('Please enter a search value. It can be a name, phone, email, address, or birthday.')
    
    search = search.strip().lower()
    found_contacts = []
    for contact in book.data.values():
        if (search in contact.name.value.lower() or
                any(search in phone.value for phone in contact.phones) or
                (contact.email and search in contact.email.value.lower()) or
                (contact.address and search in contact.address.value.lower()) or
                (contact.birthday and search in contact.get_birthday())):
            found_contacts.append(contact)
    if not found_contacts:
        return f'No contact found with the search parameter "{search}".'

    return '\n'.join(str(contact) for contact in found_contacts)

def help():
    print("")
    print("\thello - Start dialog.")
    print("")
    print("\tadd <name> <phone> - Add contact. Require name and phone.")
    print("")
    print("\tchange <name> <old phone> <new phone> - Change contact. Require name, old phone and new phone.")
    print("")
    print("\tdelete or remove <name> - Remove contact by name out from the addressbook. Require name.")
    print("")
    print("\tphone <name> - Show phone. Require name.")
    print("")
    print("\tall - Show all contacts.")
    print("")
    print("\tadd-birthday <name> <date of birthday> - Add birthday. Require name and date of birthday.")
    print("")
    print("\tshow-birthday <name> - Show birthday. Require name.")
    print("")
    print("\tbirthdays - Show birthdays next week.")
    print("")
    print("\tadd-note <name> <text> - Add note. Require name and text.")
    print("")
    print("\tedit-note <name> <text> - Edit note. Require name and text.")
    print("")
    print("\tdelete-note <name> - Delete note. Require name.")
    print("")
    print("\tfind-note <text> - Find note. Require text.")
    print("")
    print("\tshow-all-notes - Show all notes.")
    print("")
    print("\tadd-email <name> <address>- Add email. Require name and email.")
    print("")
    print("\tadd-address <name> <address> - Add address. Require name and address.")
    print("")
    print("\tadd-tags <name> <tag> - Add tags. Require name and at least one tag.")
    print("")
    print("\tsort-notes-by-tag <tag> - Sort notes by tag. Require tag.")
    print("")
    print("\tfind-note-by-tag <tag> - Find note by tag. Require tag.")
    print("")
    print("\tremove-tag <tag> - Remove tag. Require tag.")
    print("")
    print("\thelp - Show this help.")
    print("")
    print("\texit or close - Exit the program.")
    print("")

def exit_program():
    data_manager.save_all_unsaved_data()
    print("Good bye!")

def main():
    print("Welcome to the assistant bot!")
    book = data_manager.load_data(const.ADDRESS_BOOK_STORAGE_ID)
    notebook = data_manager.load_data(const.NOTEBOOK_STORAGE_ID)
    session = PromptSession(completer=command_completer, auto_suggest=AutoSuggestFromHistory(), complete_while_typing=True)
    
    while True:
        try:
            user_input = session.prompt('> ')
            command, *args = parse_input(user_input)
            
            if command in ["close", "exit"]:
                exit_program()
                print("Goodbye!")
                break
            elif command == 'hello':
                print('How can I help you?')
            elif command == 'add':
                print(add_contact(args, book))
            elif command == 'change':
                print(change_contact(args, book))
            elif command in ["delete", "remove"]:
                print(delete_contact(args, book))
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
            elif command == 'search':
                print(search_contact(args, book))
            elif command == "help" or "-h":
                help()
            else:
                print("Invalid command.")
        except Exception as e:
            print(f'Error: {e}')

if __name__ == '__main__':
    main()
