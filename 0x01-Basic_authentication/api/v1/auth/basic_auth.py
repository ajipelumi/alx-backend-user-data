#!/usr/bin/env python3
""" Basic Auth module. """
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """ Basic Auth class. """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Extract base64 authorization header. """
        # Check if authorization_header is None.
        if authorization_header is None:
            return None
        # Check if authorization_header is not a string.
        if not isinstance(authorization_header, str):
            return None
        # Check if authorization_header does not start with Basic.
        if not authorization_header.startswith('Basic '):
            return None
        # Return authorization_header without Basic.
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """ Decode base64 authorization header. """
        # Check if base64_authorization_header is None.
        if base64_authorization_header is None:
            return None
        # Check if base64_authorization_header is not a string.
        if not isinstance(base64_authorization_header, str):
            return None
        # Try to decode base64_authorization_header.
        try:
            base64_decoded = base64.b64decode(base64_authorization_header)
        except Exception:
            # If decoding fails, return None.
            return None
        # Decode decoded bytes to utf-8.
        base64_string = base64_decoded.decode('utf-8')
        # Return base64_string.
        return base64_string

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """ Extract user credentials. """
        # Check if decoded_base64_authorization_header is None.
        if decoded_base64_authorization_header is None:
            return (None, None)
        # Check if decoded_base64_authorization_header is not a string.
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        # Check if decoded_base64_authorization_header does not contain :.
        try:
            # Split decoded_base64_authorization_header by :.
            username, password = decoded_base64_authorization_header.split(':')
        except Exception:
            # If split fails, return None.
            return (None, None)
        # Return username and password as a tuple.
        return (username, password)

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ User object from credentials. """
        # Check if user_email is None or not a string.
        if user_email is None or not isinstance(user_email, str):
            return None
        # Check if user_pwd is None or not a string.
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        # Try to get user from email.
        try:
            user = User.search({'email': user_email})
        except Exception:
            # If search fails, return None.
            return None
        # Check if user is empty.
        if not user:
            return None
        # Check if user password is equal to user_pwd.
        if not user[0].is_valid_password(user_pwd):
            return None
        # Return user.
        return user[0]
