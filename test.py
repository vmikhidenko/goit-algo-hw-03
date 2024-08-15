import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
from address_book import AddressBook
from notebook import Notebook
from record import Record
from fields import DATE_FORMAT
from data_manager import DataManager
import constants as const
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

# Sample commands to test
commands = [
    'add', 'change', 'phone', 'all', 'add-birthday', 'show-birthday', 'birthdays', 
    'hello', 'close', 'exit', 'help', 'remove', 'add-note', 'edit-note', 'delete-note', 
    'find-note', 'show-all-notes', 'add-email', 'add-address', 'add-tags', 
    'sort-notes-by-tag', 'find-note-by-tag', 'remove-tag', 'search'
]

class TestAssistantBot(unittest.TestCase):
    
    def setUp(self):
        self.data_manager = DataManager()
        self.book = MagicMock(spec=AddressBook)
        self.notebook = MagicMock(spec=Notebook)
        self.session = PromptSession(completer=WordCompleter(commands, ignore_case=True), auto_suggest=AutoSuggestFromHistory(), complete_while_typing=True)
    
    @patch('builtins.print')
    def test_add_contact(self, mock_print):
        self.book.find.return_value = None
        self.book.add_record.return_value = None
        args = ['John Doe', '1234567890']
        expected_output = "Contact added."
        self.assertEqual(add_contact(args, self.book), expected_output)

    @patch('builtins.print')
    def test_change_contact(self, mock_print):
        self.book.find.return_value = MagicMock(spec=Record)
        record = self.book.find.return_value
        args = ['John Doe', '1234567890', '0987654321']
        expected_output = "Old phone 1234567890 was replaced by new phone 0987654321 for contact John Doe."
        self.assertEqual(change_contact(args, self.book), expected_output)

    @patch('builtins.print')
    def test_delete_contact(self, mock_print):
        self.book.find.return_value = MagicMock(spec=Record)
        args = ['John Doe']
        expected_output = "Contact with name \"John Doe\" successfully deleted"
        self.assertEqual(delete_contact(args, self.book), expected_output)

    @patch('builtins.print')
    def test_show_phone(self, mock_print):
        contact = MagicMock()
        contact.show_phones.return_value = '1234567890'
        self.book.find.return_value = contact
        args = ['John Doe']
        expected_output = '1234567890'
        self.assertEqual(show_phone(args, self.book), expected_output)

    @patch('builtins.print')
    def test_show_all_contacts(self, mock_print):
        self.book.data = {
            'John Doe': MagicMock(name='John Doe'),
            'Jane Doe': MagicMock(name='Jane Doe')
        }
        self.book.data['John Doe'].__str__.return_value = 'John Doe: 1234567890'
        self.book.data['Jane Doe'].__str__.return_value = 'Jane Doe: 0987654321'
        expected_output = 'John Doe: 1234567890\nJane Doe: 0987654321'
        self.assertEqual(show_all(self.book), expected_output)

    @patch('builtins.print')
    def test_add_birthday(self, mock_print):
        contact = MagicMock()
        contact.add_birthday.return_value = None
        self.book.find.return_value = contact
        args = ['John Doe', '1990-01-01']
        expected_output = "birthday 1990-01-01 successfully added to contact John Doe"
        self.assertEqual(add_birthday(args, self.book), expected_output)

    @patch('builtins.print')
    def test_show_birthday(self, mock_print):
        contact = MagicMock()
        contact.get_birthday.return_value = datetime.strptime('1990-01-01', DATE_FORMAT)
        self.book.find.return_value = contact
        args = ['John Doe']
        expected_output = "John Doe's birthday is 1990-01-01"
        self.assertEqual(show_birthday(args, self.book), expected_output)

    @patch('builtins.print')
    def test_birthdays(self, mock_print):
        contact = MagicMock()
        contact.get('name').return_value = 'John Doe'
        contact.get('congratulation_date').return_value = '1990-01-01'
        self.book.get_upcoming_birthdays.return_value = [contact]
        expected_output = "name John Doe, congratulation date: 1990-01-01"
        self.assertEqual(birthdays(self.book), expected_output)

    # Add more tests for other commands similarly.

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
