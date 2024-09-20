#!/usr/bin/env python3
"""
Contains a class for the api authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Class to manage the api authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        for ex_path in excluded_paths:
            if ex_path[-1] == "*":
                if path.startswith(ex_path[:-1]):
                    return False
            if path == ex_path or f"{path}/" == ex_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        validate all requests to secure the API
        """

        if request is None:
            return None
        auth_header = request.headers.get("Authorization")
        if auth_header is None:
            return None
        return auth_header

    def current_user(self, request=None) -> TypeVar("User"):
        return None
