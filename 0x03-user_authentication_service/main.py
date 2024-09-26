#!/usr/bin/env python3
"""
Main file
"""

from auth import Auth

email = "bob@bob.com"
password = "MyPwdOfBob"
auth = Auth()

auth.register_user(email, password)

print(auth.create_session(email))
print(auth.create_session("unknown@email.com"))
user = auth._db.find_user_by(email=email)
print(user.session_id)
print(user.id)

user_1 = auth._db.find_user_by(id=user.id)
print(user.session_id)
