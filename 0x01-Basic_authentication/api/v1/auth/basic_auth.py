#!/usr/bin/env python3
""" Basic Auth module. """
from api.v1.auth.auth import Auth
import base64


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
