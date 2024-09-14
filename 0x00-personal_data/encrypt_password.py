#!/usr/bin/env python3
"""
contains functions that hashes password
and compare with unhashed function
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    hash a password and return the hashed password
    """

    hashed_password = bcrypt.hashpw(password.encode("UTF-8"),
                                    bcrypt.gensalt())
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    return true if te hashed_password is equals to the password
    """
    if bcrypt.checkpw(password.encode("UTF-8"),
                      hashed_password):
        return True
    else:
        return False
