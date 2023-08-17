#!/usr/bin/env python3
""" Auth module. """
import bcrypt


def _hash_password(password: str) -> bytes:
    """ Returns a salted hash of the input password. """
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password with the salt
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    # Return the hashed password
    return hashed
