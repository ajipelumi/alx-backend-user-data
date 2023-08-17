#!/usr/bin/env python3
""" Auth module. """
import bcrypt
from db import DB
from user import User
import uuid
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Registers and returns a new user if email isn't listed. """
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            # Create a new user
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """ Checks if the password is valid for the email. """
        # Find the user by email and check the password
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except NoResultFound:
            # If the user doesn't exist, return False
            return False

    def create_session(self, email: str) -> str:
        """ Creates a session ID for the user email. """
        # Find the user by email
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            # If the user doesn't exist, return None
            return None
        # Create a new session ID
        session_id = _generate_uuid()
        # Update the user's session_id field
        self._db.update_user(user.id, session_id=session_id)
        # Return the session ID
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """ Finds a user instance based on a session ID. """
        # Check if session_id is None
        if session_id is None:
            return None
        # Find the user by session_id
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ Updates the corresponding user's session ID to None. """
        # Update the user's session_id field
        self._db.update_user(user_id, session_id=None)
        return None


def _hash_password(password: str) -> bytes:
    """ Returns a salted hash of the input password. """
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password with the salt
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    # Return the hashed password
    return hashed


def _generate_uuid() -> str:
    """ Returns a string representation of a new UUID. """
    return str(uuid.uuid4())
