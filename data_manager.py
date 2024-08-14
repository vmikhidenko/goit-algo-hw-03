from typing import TypeVar, Generic, Type, Dict
import pickle
from os import path

T = TypeVar('T')


class FileStorage(Generic[T]):
    def __init__(self, data_file_path: str, data_type: Type[T]):
        self._data_file_path = data_file_path
        self._data_type = data_type

    def save_data(self, data: T) -> None:
        with open(self._data_file_path, "wb") as f:
            pickle.dump(data, f)

    def load_data(self) -> T:
        if not path.exists(self._data_file_path):
            return self._data_type()
        with open(self._data_file_path, "rb") as f:
            return pickle.load(f)


class DataManager:
    def __init__(self):
        self._storages: Dict[str, FileStorage] = {}

    def add_storage(self, storage_id: str, data_file_path: str, data_type: Type[T]) -> None:
        if storage_id in self._storages:
            raise ValueError(f"Storage with ID {storage_id} already exists.")

        storage = FileStorage(data_file_path, data_type)
        self._storages[storage_id] = storage

    def save_data(self, storage_id: str, data: T) -> None:
        storage = self._storages.get(storage_id)
        if storage is None:
            raise ValueError(f"No storage found for storage ID {storage_id}")
        storage.save_data(data)

    def load_data(self, storage_id: str) -> T:
        storage = self._storages.get(storage_id)
        if storage is None:
            raise ValueError(f"No storage found for storage ID {storage_id}")
        return storage.load_data()
