#!/usr/bin/env python3
""" Session Exp Auth module. """
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """ Session Exp Auth class. """
    def __init__(self):
        """ Initialize Session Exp Auth. """
        super().__init__()
        # Get session duration.
        session_duration_string = getenv("SESSION_DURATION")
        # Cast session duration to int.
        try:
            self.session_duration = int(session_duration_string)
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """ Create session. """
        # Create session_id.
        session_id = super().create_session(user_id)
        # Check if session_id is None.
        if session_id is None:
            return None
        # Create session dictionary.
        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        # Add session dictionary to user_id_by_session_id attribute.
        self.user_id_by_session_id[session_id] = session_dictionary
        # Return session_id.
        return session_id


def user_id_for_session_id(self, session_id: str = None) -> str:
    """ User ID for session ID. """
    # Check if session_id is None.
    if session_id is None:
        return None
    # Check if user_id_by_session_id has session_id.
    if session_id not in self.user_id_by_session_id:
        return None
    # Check if session_duration is equal or less than 0.
    if self.session_duration <= 0:
        return self.user_id_by_session_id.get(session_id).get("user_id")
    # Check if session_duration contains the created_at key.
    if "created_at" not in self.user_id_by_session_id.get(session_id):
        return None
    # Get current time.
    current_time = datetime.now()
    # Get session time.
    session_time = self.user_id_by_session_id.get(session_id).get("created_at")
    # Get expiration time.
    expiration_time = session_time + timedelta(seconds=self.session_duration)
    # Check if user session is expired.
    if expiration_time < current_time:
        return None
    # Return user_id.
    return self.user_id_by_session_id.get(session_id).get("user_id")
