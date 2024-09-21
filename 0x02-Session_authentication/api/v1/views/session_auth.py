#!/usr/bin/env python3
"""
handles all routes for the Session Authentication
"""

from api.v1.views import app_views
from flask import jsonify, request
from models.user import User
from models.user_session import UserSession
import os


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def login():
    """
    authenticate the user using email and password
    """

    user_email = request.form.get("email")
    if user_email is None:
        return jsonify({
            "error": "email missing"
            }), 400
    user_pwd = request.form.get("password")
    if user_pwd is None:
        return jsonify({
            "error": "password missing"
            }), 400

    users = User.search({"email": user_email})
    if users is None or users == []:
        return jsonify({
            "error": "no user found for this email"
            }), 404
    real_user = None
    for user in users:
        if user.is_valid_password(user_pwd):
            real_user = user
            break
    if real_user is None:
        return jsonify({
            "error": "wrong password"
            }), 401
    from api.v1.app import auth
    session_id = auth.create_session(real_user.id)
    user_json = jsonify(real_user.to_json())
    session_name = os.getenv("SESSION_NAME")
    user_json.set_cookie(session_name, session_id)
    return user_json


@app_views.route("/auth_session/logout",
                 methods=["DELETE"], strict_slashes=False)
def logout():
    """
    logout the user out and delete the user session id
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    else:
        abort(404)
