from flask import Blueprint, request, jsonify
from config import users_collection
import bcrypt


auth_bp = Blueprint(
    "auth",
    __name__
)


@auth_bp.route(
    "/signup",
    methods=["POST"]
)
def signup():

    try:

        data = request.get_json()

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username:
            return jsonify({
                "success": False,
                "message": "Username required"
            }), 400

        if not email:
            return jsonify({
                "success": False,
                "message": "Email required"
            }), 400

        if not password:
            return jsonify({
                "success": False,
                "message": "Password required"
            }), 400

        existing_user = users_collection.find_one(
            {"email": email}
        )

        if existing_user:

            return jsonify({
                "success": False,
                "message": "Email already registered"
            }), 409

        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        )

        users_collection.insert_one(
            {
                "username": username,
                "email": email,
                "password": hashed_password
            }
        )

        return jsonify({
            "success": True,
            "message": "User registered successfully"
        }), 201

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


@auth_bp.route(
    "/login",
    methods=["POST"]
)
def login():

    try:

        data = request.get_json()

        email = data.get("email")
        password = data.get("password")

        if not email:
            return jsonify({
                "success": False,
                "message": "Email required"
            }), 400

        if not password:
            return jsonify({
                "success": False,
                "message": "Password required"
            }), 400

        user = users_collection.find_one(
            {"email": email}
        )

        if not user:

            return jsonify({
                "success": False,
                "message": "User not found"
            }), 404

        password_match = bcrypt.checkpw(
            password.encode("utf-8"),
            user["password"]
        )

        if not password_match:

            return jsonify({
                "success": False,
                "message": "Invalid password"
            }), 401

        return jsonify({
            "success": True,
            "message": "Login successful",
            "user": {
                "id": str(user["_id"]),
                "username": user["username"],
                "email": user["email"]
            }
        }), 200

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


@auth_bp.route(
    "/users",
    methods=["GET"]
)
def get_users():

    users = []

    for user in users_collection.find():

        users.append(
            {
                "id": str(user["_id"]),
                "username": user["username"],
                "email": user["email"]
            }
        )

    return jsonify(users)