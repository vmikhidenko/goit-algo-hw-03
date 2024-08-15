# Assistant Bot

## Overview

This is an assistant bot that allows you to manage contacts and notes. It offers various features like adding, editing, and deleting contacts, storing their birthdays, and managing notes with tags. The bot also includes a command-line interface with auto-suggestion and command completion to facilitate user interaction.

## Features

- **Contact Management:**
  - Add new contacts with names, addresses, phone numbers, emails, and birthdays.
  - Search contacts by various criteria (e.g., name, phone number, email, address, birthday).
  - Edit and delete existing contacts.
  - Display contacts with upcoming birthdays within a specified period.
  - Validate phone numbers and email addresses during addition or editing.
  
- **Note Management:**
  - Add, edit, delete, and search text notes.
  - Tag notes with specific keywords.
  - Search and sort notes by tags.

- **Data Persistence:**
  - All data (contacts, notes) are saved on the hard drive in the user's directory.
  - The assistant can be restarted without losing data.

- **User Interaction:**
  - Autocomplete commands with a user-friendly command-line interface.
  - The bot can guess the user's intended command based on the input text and suggest the closest matching command.

## Installation

1. Clone the repository to your local machine.
2. Ensure you have Python 3.7+ installed.
3. Install the required dependencies by running:
   ```bash
   pip install -r requirements.txt
4. In order to install the bot run a command from terminal command line: 
    ```bash 
    pip install -e .

Commands
Contact Management
add <name> <phone>: Add a new contact with the specified name and phone number.
change <name> <old phone> <new phone>: Change the phone number of an existing contact.
delete <name>: Remove a contact by name.
phone <name>: Display the phone number of the specified contact.
all: Show all contacts.
add-birthday <name> <date>: Add a birthday to an existing contact.
show-birthday <name>: Display the birthday of the specified contact.
birthdays: Show contacts with birthdays within the next 7 days.
add-email <name> <email>: Add an email to an existing contact.
add-address <name> <address>: Add an address to an existing contact.
search <query>: Search for a contact by name, phone number, email, address, or birthday.
Note Management
add-note <title> <text>: Add a new note with the specified title and text.
edit-note <title> <new text>: Edit the text of an existing note.
delete-note <title>: Delete a note by title.
find-note <text>: Search for a note containing the specified text.
show-all-notes: Display all notes.
add-tags <title> <tag>: Add tags to an existing note.
sort-notes-by-tag <tag>: Sort notes by a specific tag.
find-note-by-tag <tag>: Find notes that have the specified tag.
remove-tag <tag>: Remove a tag from all notes.
Utility Commands
hello: Start a conversation with the bot.
help: Display a list of available commands and their descriptions.
exit or close: Save all data and exit the program.
Data Storage
The assistant bot uses a DataManager to manage data persistence. Contacts and notes are stored in separate files on the hard drive. Data is automatically saved when the program exits, ensuring no data loss between sessions.

Error Handling
The bot uses decorators to handle input errors and provides helpful messages when commands are used incorrectly. It also ensures data integrity by validating phone numbers and email addresses during input.