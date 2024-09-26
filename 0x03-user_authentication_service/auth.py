#!/usr/bin/evn python3
"""
contains Auth class and function
to hash a password
"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> str:
    """
    hash the password string
    """
    return bcrypt.hashpw(password.encode("UTF-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    generate a uuid and return the string
    """
    return str(uuid4())


class Auth:
    """ Auth class to interact with the authentication database
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a user and add it to the database
        """

        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password
                                     (password))
        else:
            raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """
        locate the user by email and if exists, it check the password
        with the user password, if correct, return True otherwise
        return False
        """

        try:
            user = self._db.find_user_by(email=email)
        except Exception as e:
            return False
        else:
            if bcrypt.checkpw(password.encode("UTF-8"), user.hashed_password):
                return True
            else:
                return False

    def create_session(self, email: str) -> str:
        """
        takes an email string argument and returns the
        session ID as a string
        """

        try:
            user = self._db.find_user_by(email=email)
        except Exception as e:
            return None
        else:
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        takes in a single session_id string as argument and return
        the corresponding user or None
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except Exception as e:
            return None
        else:
            return user

    def destroy_session(self, user_id: int) -> None:
        """
        updates the corresponding user's session ID to None
        """
        if user_id is None:
            return None
        try:
            self._db.update_user(user_id, session_id=None)
        except Exception as e:
            return None
        else:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """
        takes in an email string as an input, then generate a UUID
        and update the user's reset_token database field
        and return the string
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception as e:
            raise ValueError
        else:
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        update the user password from the database
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except Exception:
            raise ValueError
        else:
            hashed_password = _hash_password(password)
            self.update_user(user.id, hashed_password=hashed_password,
                             reset_token=None)
            return None
