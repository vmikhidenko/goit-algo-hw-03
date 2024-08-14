from decorators import input_error
from collections import UserDict
from typing import List

class Note():
  def __init__(self, name: str, text: str):
    self.name = name
    self.text = text

  def edit(self, new_text: str) -> None:
    self.text = new_text

  def __str__(self) -> str:
    return f"name: {self.name}; text: {self.text}"

class Notebook(UserDict):
  def __init__(self):
    super().__init__()
    self.last_id = 0

  def add_note(self, note: Note) -> str:
    self.last_id += 1
    self.data[self.last_id] = note
  
  def find_by_name(self, name: str) -> Note | None:
    for note in self.data.values():
      if (note.name == name):
        return note

    return None
  
  def edit_note(self, name: str, new_text: str) -> Note | None:
    note = self.find_by_name(name)
    if not note:
      return None
    
    note.edit(new_text)
    return note

  def delete_note(self, name: str) -> Note | None:
    for id, note in self.data.items():
      if note.name == name:
        del self.data[id]
        return note
    
    return None

  def find_by_text(self, text: str) -> List[Note] | None:
    result = []
    text_lower = text.lower()
    
    for note in self.data.values():
      if text_lower in note.name.lower() or text_lower in note.text.lower():
        result.append(note)
    
    return result if len(result) > 0 else None


@input_error
def add_note_command(args, notebook: Notebook) -> str:
  name, text = args
  
  if not name:
    raise ValueError('You need to specify name of your note')
  if not text:
    raise ValueError('You need to specify text of your note')
  
  note = notebook.find_by_name(name)
  if note:
    return f"Your notebook already contains a note with name '{name}'"

  note = Note(name, text)
  notebook.add_note(note)

  return f"New note with name '{name}' has been successfully added to your notebook"

@input_error
def edit_note_command(args, notebook: Notebook) -> str:
  name, text = args

  if not name:
    raise ValueError('You need to specify name note to edit')
  if not text:
    raise ValueError('You need to specify text note to edit')
  
  note = notebook.edit_note(name, text)

  if not note:
    return f"Note with name '{name}' was not found in your notebook"
  
  return f"Note with name '{name}' has been successfully edited"

@input_error
def delete_note_command(args, notebook: Notebook) -> str:
  name, = args

  if not name:
    raise ValueError('You need to specify name of note to delete')
  
  note = notebook.delete_note(name)

  if not note:
    return f"Note with name '{name}' was not found in your notebook"
  
  return f"Note with name '{name}' has been successfully deleted"

@input_error
def find_note_command(args, notebook: Notebook) -> str:
  text, = args

  if not text:
    raise ValueError('you need specify search pattern')
  
  notes = notebook.find_by_text(text)

  if not notes:
    return f"Nothing found"
  
  result = "This is the list of found notes:\n"
  result += '\n'.join(map(lambda note: note.__str__(),  notes))
  return result

@input_error
def show_all_notes_command(notebook: Notebook) -> str:
  result = []
  for id, note in notebook.data.items():
    result.append(f"{id}) {note}")

  return "You don't have notes at the moment" if len(result) == 0 else '\n'.join(result)
