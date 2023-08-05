#!/usr/bin/env python3
""" Encrypt password module. """
import bcrypt


def hash_password(password: str) -> bytes:
    """ Encrypts a password. """
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password with the salt
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    # Return the hashed password
    return hashed
