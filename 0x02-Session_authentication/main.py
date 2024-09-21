#!/usr/bin/env python3
""" main
"""

from api.v1.auth.session_db_auth import SessionDBAuth
from models.user import User
from models.user_session import UserSession

sa = SessionDBAuth()
user = User()
user_email = "bobsession@hbtn.io"
user_clear_pwd = "fake pwd"
user.email = user_email
user.password = user_clear_pwd
user.save()

print(f"User id: {user.id}")
session_id = sa.create_session(user.id)

print(f"Session ID: {session_id}")
usr_id = sa.user_id_for_session_id(session_id)
print("User Id gotten from sa: {}".format(usr_id))
