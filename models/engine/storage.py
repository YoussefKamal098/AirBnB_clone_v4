#!/usr/bin/python3
"""
This module defines the abstract Storage class,
which serves as the interface for interacting with
different storage mechanisms.
"""
from abc import ABC, abstractmethod

from models.engine.stored_classes import CLASSES


class Storage(ABC):
    __CLASSES = CLASSES

    @abstractmethod
    def all(self, cls=None):
        """Retrieve all objects of a given class or all classes."""
        pass

    @abstractmethod
    def new(self, obj):
        """Add a new object to the storage."""
        pass

    @abstractmethod
    def save(self):
        """Commit changes to the storage."""
        pass

    @abstractmethod
    def reload(self):
        """Reload data from the storage."""
        pass

    @abstractmethod
    def delete(self, obj=None):
        """Delete an object from the storage."""
        pass

    @abstractmethod
    def find(self, class_name, _id):
        """Find an object by its class name and ID."""
        pass

    def get(self, cls, _id):
        """
        Get an object by its class and ID
        Parameters:
            cls (BaseModel): the class of the object
            _id (str): the ID of the object
        Returns:
            The object if found, otherwise None
        """
        if not cls or cls not in self.get_classes():
            return None

        return self.find(cls.__name__, _id)

    def count(self, cls=None):
        """
        Count the number of objects of a given class or all classes
        Parameters:
            cls (BaseModel): the class to count
        Returns:
            The number of objects of the given class or
            all classes if cls is None or 0 if the class is not found (int)
        """
        if not cls:
            return sum(
                self.count_by_class_name(cls.__name__)
                for cls in self.get_classes()
            )

        if cls not in self.get_classes():
            return 0

        return self.count_by_class_name(cls.__name__)

    @abstractmethod
    def find_all(self, class_name=""):
        """Find all objects of a given class."""
        pass

    @abstractmethod
    def update(self, obj=None, attr=None, value=None):
        """Update an object's attribute."""
        pass

    @abstractmethod
    def count_by_class_name(self, class_name):
        """Count the number of objects of a given class."""
        pass

    @abstractmethod
    def close(self):
        """Close the storage session."""
        pass

    @staticmethod
    def _get_obj_key(class_name, _id):
        """
        Generates a unique key for an object based on class name and ID
        Parameters:
            class_name (str): the name of the class
            _id (str): the ID of the object
        Returns:
            The generated key (str)
        """
        if not class_name or not _id:
            return None

        return "{}.{}".format(class_name, _id)

    def get_classes(self):
        """Returns a tuple of classes"""
        return tuple(self.__CLASSES.values())

    def get_classes_names(self):
        """Returns a tuple of model names"""
        return tuple(self.__CLASSES.keys())

    def get_class(self, class_name):
        """
        Returns the class corresponding to a class name
        Parameters:
            class_name (str): the name of the class
        Returns:
            The class if found (BaseModel), otherwise None
        """
        if class_name not in self.get_classes_names():
            return None

        return self.__CLASSES.get(class_name)
