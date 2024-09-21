#!/usr/bin/env python3
"""
Implement a session authentication system
"""
import uuid
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """
    a session authentication system that is stored
    in the database
    """
    def __init__(self):
        """ Initialize the SessionDBAuth instance
        """
        super().__init__()

    def create_session(self, user_id: str = None) -> str:
        """
        create a Session ID for user ID and
        instantiate a UserSession class to save to file
        """
        if user_id is None or type(user_id) is not str:
            return None
        user_session = UserSession()
        user_session.user_id = user_id
        user_session.session_id = user_session.id
        user_session.save()
        return user_session.id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        return User ID based on a session ID
        """
        if session_id is None or type(session_id) is not str:
            return None
        user_session = UserSession.get(session_id)
        if user_session is None:
            return None
        if self.session_duration <= 0:
            return user_session.user_id
        exp = timedelta(seconds=self.session_duration)
        date = user_session.created_at + exp
        if date < datetime.utcnow():
            return None
        return user_session.user_id

    def destroy_session(self, request: str = None) -> bool:
        """
        delete the user session/logout
        """
        if request is None or type(request) is not str:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        user_session = UserSession.get(session_id)
        user.session.remove()
        return True
