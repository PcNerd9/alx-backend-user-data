#!/usr/bin/env python3
"""
Contains a Basic Authentication system
"""
from api.v1.auth.auth import Auth
import base64
import hashlib
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """
    For Basic Authentication
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        returns the Base64 part of the authorization header
        for a basic authentication
        """

        if authorization_header is None:
            return None
        if type(authorization_header) != str:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split()[1]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """
        returns the decoded value of a Base64 string
        """

        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) != str:
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header)
            return decoded.decode("UTF-8")
        except Exception as e:
            return None

    def extract_user_credentials(
            self,
            decode_base64_authorization_header: str) -> (str, str):
        """
        returns the user email and password from the
        Base64 decoded value
        """

        if decode_base64_authorization_header is None:
            return None, None
        if type(decode_base64_authorization_header) != str:
            return None, None
        if ":" not in decode_base64_authorization_header:
            return None, None
        data = decode_base64_authorization_header.split(":", 1)
        return (data[0], data[1])

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar("User"):
        """
        returns the User instance based on his email and password
        """

        if user_email is None or type(user_email) != str:
            return None
        if user_pwd is None or type(user_pwd) != str:
            return None
        attribute = {"email": user_email}
        users = User.search(attribute)
        if users is None or users == []:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request: str = None) -> TypeVar("User"):
        """
        overload the Auth and retrieves the User instance for a request
        """
        auth_header = self.authorization_header(request)
        extracted_header = self.extract_base64_authorization_header(
                auth_header)

        if extracted_header is None:
            return None
        decoded_header = self.decode_base64_authorization_header(
                extracted_header)
        if decoded_header is None:
            return None
        user_credentials = self.extract_user_credentials(decoded_header)
        if not user_credentials:
            return None
        return self.user_object_from_credentials(
                user_email=user_credentials[0],
                user_pwd=user_credentials[1])
