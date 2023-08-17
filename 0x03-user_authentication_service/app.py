#!/usr/bin/env python3
""" Flask app module. """
from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
