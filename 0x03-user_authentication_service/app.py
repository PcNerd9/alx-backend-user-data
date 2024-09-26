#!/usr/bin/env python3

"""
The flask app for the application
"""
from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def home():
    """
    the home page
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """
    register a user
    """
    user_email = request.form.get("email")
    user_pwd = request.form.get("password")

    try:
        user = AUTH.register_user(user_email, user_pwd)
    except ValueError:
        return jsonify({
                "message": "email already registered"
                }), 400
    else:
        return jsonify({
            "email": user.email,
            "message": "user created"
            })


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """
    login a user and set a session_id cookie
    """

    user_email = request.form.get("email")
    user_pwd = request.form.get("password")
    if not user_email or not user_pwd:
        abort(401)

    if AUTH.valid_login(email=user_email, password=user_pwd):
        session_id = AUTH.create_session(email=user_email)
    else:
        abort(401)
    out = jsonify({
        "email": user_email,
        "message": "logged in"
        })
    out.set_cookie("session_id", session_id)
    return out


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """
    destroy user session
    """
    session_id = request.cookies.get("session_id")
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect(url_for("home"))


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile():
    """
    get user using it's session id from cookie value
    """
    session_id = request.cookies.get("session_id")
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({
        "email": user.email
        })


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def reset_password():
    """
    generate a reset_token and send it to the user
    """
    user_email = request.form.get("email")
    if user_email is None:
        abort(403)

    try:
        reset_token = AUTH.get_reset_password_token(user_email)
    except ValueError:
        abort(403)
    else:
        return jsonify({
            "email": user_email,
            "reset_token": reset_token
            })


@app.route("/update_password", methods=["PUT"], strict_slashes=False)
def update_password():
    """
    update the password of the user from the database
    """
    reset_token = request.form.get("reset_token")
    user_email = request.form.get("email")
    password = request.form.get("new_password")

    try:
        AUTH.update_password(reset_token=reset_token, password=password)
    except ValueError:
        abort(403)
    else:
        return jsonify({
            "email": email,
            "message": "Password updated"
            }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
