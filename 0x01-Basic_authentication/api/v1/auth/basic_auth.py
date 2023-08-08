#!/usr/bin/env python3
""" Basic Auth module. """
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ Basic Auth class. """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
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
