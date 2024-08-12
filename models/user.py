#!/usr/bin/python3
"""
This module defines the User class, which inherits from the BaseModel class.
"""
import os
import hashlib

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel, Base

STORAGE_TYPE = os.getenv('HBNB_TYPE_STORAGE')

parent_classes = (
    BaseModel,
    Base if STORAGE_TYPE == "db" else object
)


class User(*parent_classes):
    """
    User class represents a user.
    """
    NOT_UPDATABLE = ['email']

    if STORAGE_TYPE == "db":
        __tablename__ = 'users'

        email = Column(String(128), nullable=False, index=True)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), index=True)
        last_name = Column(String(128), index=True)
        places = relationship('Place', back_populates='user',
                              passive_deletes=True)
        reviews = relationship('Review', back_populates='user',
                               passive_deletes=True)

    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """
        Initializes a new User instance. If a password is provided,
        it is hashed before being stored.

        Parameters:
        - *args: Variable-length argument list.
        - **kwargs: Arbitrary keyword arguments.
        """
        if "password" in kwargs:
            kwargs["password"] = self.hash_password(kwargs["password"])

        super().__init__(*args, **kwargs)

    def to_dict(self):
        """
        Returns a dictionary representation of the User instance.

        Returns:
        - A dictionary containing the User information.
        """
        user_dict = super().to_dict()
        user_dict.pop("password", None)
        return user_dict

    def hash_password(self, pwd):
        """
        Hashes a password using the MD5 algorithm.

        Parameters:
        - pwd: The password to hash.

        Returns:
        - The hashed password.
        """
        return hashlib.md5(pwd.encode()).hexdigest()
