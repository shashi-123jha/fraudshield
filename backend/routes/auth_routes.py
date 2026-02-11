from flask import Blueprint
from auth import signup, login

auth_routes = Blueprint("auth_routes", __name__)

auth_routes.route("/signup", methods=["POST"])(signup)
auth_routes.route("/login", methods=["POST"])(login)
