#!/usr/bin/env python3
""" Flask app module. """
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome() -> str:
    """ GET /
    Return:
      - Welcome message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user() -> str:
    """ POST /users
    JSON body:
      - email
      - password
      Return:
      - User registered.
    """
    # Get the JSON
    email = request.form.get('email')
    password = request.form.get('password')
    # Try to register the user
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": "{}".format(email),
                        "message": "user created"})
    except ValueError:
        # User already registered if ValueError
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def log_in() -> str:
    """ POST /sessions
    JSON body:
      - email
      - password
      Return:
      - Logged in user.
    """
    # Get the JSON
    email = request.form.get('email')
    password = request.form.get('password')
    # Check if the email and password match
    if AUTH.valid_login(email, password):
        # Create a new session ID
        session_id = AUTH.create_session(email)
        # Create response JSON body
        response = jsonify({"email": "{}".format(email),
                            "message": "logged in"})
        # Set the cookie
        response.set_cookie("session_id", session_id)
        return response
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def log_out() -> str:
    """ DELETE /sessions
    JSON body:
      - session_id
    Return:
      - Destroy session and redirect user to GET /
    """
    # Get the session ID
    session_id = request.cookies.get('session_id')
    # Get the user from the session ID
    user = AUTH.get_user_from_session_id(session_id)
    # If the user exists destroy the session and redirect to GET /
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    else:
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """ GET /profile
    JSON body:
      - session_id
    Return:
      - User profile.
    """
    # Get the session ID
    session_id = request.cookies.get('session_id')
    # Get the user from the session ID
    user = AUTH.get_user_from_session_id(session_id)
    # If the user exists return the user profile
    if user:
        return jsonify({"email": "{}".format(user.email)}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """ POST /reset_password
    JSON body:
      - email
    Return:
      - Reset token.
    """
    # Get the JSON
    email = request.form.get('email')
    # Try to get the reset token
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": "{}".format(email),
                        "reset_token": "{}".format(reset_token)}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
