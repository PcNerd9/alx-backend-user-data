#!/usr/bin/env python3
"""
implement a user session class
"""

from models.base import Base
from typing import List


class UserSession(Base):
    """
    a model for the session authentication system
    """

    def __init__(self, *args: List, **kwargs: dict):
        """
        Initialize a UserSession instance
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id")
