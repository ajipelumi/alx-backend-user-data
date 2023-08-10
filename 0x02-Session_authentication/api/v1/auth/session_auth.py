#!/usr/bin/env python3
""" Session Auth module. """
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """ Session Auth Class. """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Create session. """
        # Check if user_id is None.
        if user_id is None:
            return None
        # Check if user_id is not a string.
        if not isinstance(user_id, str):
            return None
        # Create session_id.
        session_id = uuid.uuid4()
        # Add session_id to user_id_by_session_id attribute.
        self.user_id_by_session_id[session_id] = user_id
        # Return session_id.
        return session_id
