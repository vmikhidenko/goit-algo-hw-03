from decorators import input_error
from collections import UserDict
from typing import List


class Note:

    def __init__(self, name: str, text: str, tags: List[str] = None):
        self.name = name
        self.text = text
        self.tags = tags if tags else []

    def edit(self, new_text: str) -> None:
        self.text = new_text

    def add_tags(self, new_tags: List[str]) -> None:
        self.tags.extend(new_tags)

    def remove_tag(self, tag: str) -> None:
        if tag in self.tags:
            self.tags.remove(tag)
        else:
            raise ValueError(f"Tag '{tag}' not found in note '{self.name}'")

    def __str__(self) -> str:
        return f"name: {self.name}; text: {self.text}; tags: {self.tags}"


class Notebook(UserDict):
    def __init__(self):
        super().__init__()
        self.last_id = 0

    def add_note(self, note: Note) -> str:
        self.last_id += 1
        self.data[self.last_id] = note

    def find_by_name(self, name: str) -> Note | None:
        for note in self.data.values():
            if note.name == name:
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

    def add_tags_to_note(self, name: str, tags: List[str]) -> Note | None:
        note = self.find_by_name(name)
        if not note:
            return None

        note.add_tags(tags)
        return note

    def find_by_tag(self, tag: str) -> List[Note] | None:
        result = []
        for note in self.data.values():
            if tag in note.tags:
                result.append(note)

        return result if len(result) > 0 else None

    def sort_notes_by_tag(self, tag: str) -> List[Note] | None:
        return sorted(self.find_by_tag(tag), key=lambda note: note.name)

    def remove_tag_from_note(self, name: str, tag: str) -> Note | None:
        note = self.find_by_name(name)
        if not note:
            return None

        note.remove_tag(tag)
        return note


@input_error
def add_note_command(args, notebook: Notebook) -> str:
    name, text = args

    if not name:
        raise ValueError("You need to specify name of your note")
    if not text:
        raise ValueError("You need to specify text of your note")

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
        raise ValueError("You need to specify name note to edit")
    if not text:
        raise ValueError("You need to specify text note to edit")

    note = notebook.edit_note(name, text)

    if not note:
        return f"Note with name '{name}' was not found in your notebook"

    return f"Note with name '{name}' has been successfully edited"


@input_error
def delete_note_command(args, notebook: Notebook) -> str:
    (name,) = args

    if not name:
        raise ValueError("You need to specify name of note to delete")

    note = notebook.delete_note(name)

    if not note:
        return f"Note with name '{name}' was not found in your notebook"

    return f"Note with name '{name}' has been successfully deleted"


@input_error
def find_note_command(args, notebook: Notebook) -> str:
    (text,) = args

    if not text:
        raise ValueError("you need specify search pattern")

    notes = notebook.find_by_text(text)

    if not notes:
        return f"Nothing found"

    result = "This is the list of found notes:\n"
    result += "\n".join(map(lambda note: note.__str__(), notes))
    return result


@input_error
def show_all_notes_command(notebook: Notebook) -> str:
    result = []
    for id, note in notebook.data.items():
        result.append(f"{id}) {note}")

    return (
        "You don't have notes at the moment" if len(result) == 0 else "\n".join(result)
    )


@input_error
def add_tags_command(args, notebook: Notebook) -> str:
    name, *tags = args
    if not name or not tags:
        raise ValueError("You need to specify note name and at least one tag")

    note = notebook.add_tags_to_note(name, tags)
    if not note:
        return f"Note with name '{name}' was not found in your notebook"

    return f"Tags {', '.join(tags)} were added to note '{name}'"


@input_error
def find_note_by_tag_command(args, notebook: Notebook) -> str:
    (tag,) = args
    if not tag:
        raise ValueError("You need to specify a tag to search for")

    notes = notebook.find_by_tag(tag)
    if not notes:
        return f"No notes found with tag '{tag}'"

    result = "Notes with the specified tag:\n"
    result += "\n".join(map(lambda note: note.__str__(), notes))
    return result


@input_error
def sort_notes_by_tag_command(args, notebook: Notebook) -> str:
    (tag,) = args
    if not tag:
        raise ValueError("You need to specify a tag to sort by")

    notes = notebook.sort_notes_by_tag(tag)
    if not notes:
        return f"No notes found with tag '{tag}'"

    result = "Sorted notes by tag:\n"
    result += "\n".join(map(lambda note: note.__str__(), notes))
    return result


@input_error
def remove_tag_command(args, notebook: Notebook) -> str:
    name, tag = args
    if not name or not tag:
        raise ValueError("You need to specify the note name and the tag to remove")

    note = notebook.remove_tag_from_note(name, tag)
    if not note:
        return f"Note with name '{name}' was not found in your notebook"

    return f"Tag '{tag}' was removed from note '{name}'"
