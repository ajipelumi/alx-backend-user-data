#!/usr/bin/env python3
""" Flask app module. """
from flask import Flask, jsonify, request, abort
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
