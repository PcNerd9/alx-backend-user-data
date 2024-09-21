#!/usr/bin/env python3
"""
Contains A session with expiration
"""

from api.v1.auth.session_auth import SessionAuth
from models.user import User
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """
    Implement a Session Authentication
    with expiration
    """

    def __init__(self):
        var = os.getenv("SESSION_DURATION")
        if var:
            try:
                self.session_duration = int(var)
            except Exception as e:
                self.session_duration = 0
        else:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """
        creates a session ID for a user ID
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
                "user_id": user_id,
                "created_at": datetime.now()
                }
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        returns a user id based on session id
        """

        if session_id is None:
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None
        if self.session_duration <= 0:
            return session_dict.get("user_id")
        if session_dict.get("created_at") is None:
            return None
        exp = timedelta(seconds=self.session_duration)
        date = session_dict.get("created_at") + exp
        if date < datetime.utcnow():
            return None
        return session_dict.get("user_id")
