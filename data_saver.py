import pickle
from address_book import AddressBook
from notebook import Notebook

FILE_NAME="addressbook.pkl"
NOTES_FILE_NAME="notes.pkl"

class Data_saver():
  def save_data(self, book):
    with open(FILE_NAME, "wb") as fh:
      pickle.dump(book, fh)

  def load_data(self):
    try:
      with open(FILE_NAME, "rb") as fh:
        return pickle.load(fh)
    except FileNotFoundError:
      return AddressBook()
    
  def load_notebook(self):
    try:
      with open(NOTES_FILE_NAME, "rb") as fh:
        return pickle.load(fh)
    except FileNotFoundError:
      return Notebook()
    
  def save_notebook(self, notebook: Notebook):
    with open(NOTES_FILE_NAME, "wb") as fh:
      pickle.dump(notebook, fh)



data_saver = Data_saver()
