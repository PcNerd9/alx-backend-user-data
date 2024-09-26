#!/usr/bin/env python3
"""
Main file
"""
import requests


def register_user(email: str, password: str) -> None:
    """
    test POST request to /users route
    """
    data = {
            "email": email,
            "password": password
            }
    url = "http://localhost:5000/users"
    response = requests.post(url=url, data=data)
    data = response.json()
    assert response.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    """
    test the POST request to /session route
    """

    data = {
            "email": email,
            "password": password
            }
    url = "http://localhost:5000/sessions"
    response = requests.post(url=url, data=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> None:
    """
    test the POST request to /sesson route with
    correct details
    """
    data = {
            "email": email,
            "password": password
            }
    url = "http://localhost:5000/sessions"
    response = requests.post(url=url, data=data)
    assert response.status_code == 200
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """
    test GET request to the /profile route
    without setting the cookie
    """
    url = "http://localhost:5000/profile"
    response = requests.get(url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    test the GET  request to the /profile route
    with the cookie set
    """
    cookie = {"session_id": session_id}
    url = "http://localhost:5000/profile"
    response = requests.get(url=url, cookies=cookie)
    assert response.status_code == 200


def log_out(session_id: str) -> None:
    """
    test the DELETE request to /sessions route
    to test the log_out method returns the expected status
    """
    cookie = {"session_id": session_id}
    url = "http://localhost:5000/sessions"
    response = requests.delete(url=url, cookies=cookie)
    assert response.status_code == 200


def reset_password_token(email: str) -> None:
    """
    test the POST request to /reset_password route
    """
    data = {"email": email}
    url = "http://localhost:5000/reset_password"
    response = requests.post(url=url, data=data)
    assert response.status_code == 200
    return response.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    test the PUT request to the update_password route to ensure
    it returns the excepted status_code
    """
    data = {
            "email": email,
            "reset_token": reset_token,
            "new_password": new_password
            }
    url = "http://localhost:5000/update_password"
    response = requests.put(url, data=data)
    assert response.status_code == 200


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
