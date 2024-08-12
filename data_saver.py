import pickle
from address_book import AddressBook

FILE_NAME="addressbook.pkl"

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


data_saver = Data_saver()
