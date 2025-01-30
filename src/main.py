#!/usr/bin/env python

from flask import Flask, redirect
from flask_restful import Api, Resource
from psycopg.connection import Connection
from psycopg.rows import TupleRow
from psycopg import connect as psql_connect
from werkzeug.wrappers import Response

from backend.database.setup import initialise_tables
from lib.instilled.instiled import Instil

from lib.jwt.jwt import Jwt
from lib.swagdoc.swagmanager import SwagManager
from lib.swagdoc.swagtag import SwagTag
from routes.user.profile import Profile
from routes.user.subscriptions import Subscriptions
from routes.org.module import user
from routes.auth.register import CheckEmail, CheckUsername, Register
from routes.auth.login import Login
from routes.auth.verify2fa import Verify2FA
from routes.auth.verify_email import VerifyEmail, ConfirmEmail
app: Flask = Flask(__name__)
api: Api = Api(app)
swag: SwagManager = SwagManager(
    app,
    "Python TSE backend API",
    "Examples of how to use the projects python API",
    "0.0.0",
)

# TODO: Add docker container detection for which to use
ip_url: str = "postgres"  # 127.0.0.1

conn: Connection[TupleRow] = psql_connect(
    f"postgresql://postgres:cisco@{ip_url}:5432/dev"
)
print("Database connected")
initialise_tables(conn)  # create tables if they don't exist
print("Initialized tables")

Instil.add_service("db", conn)
print("Registered database service")


class Main(Resource):

    def get(self) -> Response:
        return redirect("/apidocs")


api.add_resource(Main, "/")
api.add_resource(Subscriptions, "/v1/user/<int:user_id>/subscriptions")
api.add_resource(Profile, "/v1/user/<int:user_id>/profile")
api.add_resource(
    user.User, "/v1/org/<int:org_id>/module/<int:module_id>/user/<int:user_id>")
api.add_resource(CheckEmail, "/v1/auth/email")
api.add_resource(CheckUsername, '/v1/auth/username')
api.add_resource(Register, '/v1/auth/register')
api.add_resource(Login, '/v1/auth/login')
api.add_resource(Verify2FA, '/v1/auth/2fa')
api.add_resource(VerifyEmail, '/v1/auth/verify-email')


swag.add_tag(SwagTag("Organisation", "Organisation related endpoints"))
swag.add_tag(SwagTag("Module", "Module related endpoints"))
swag.add_tag(SwagTag("User", "User related endpoints"))
swag.add_swag(Subscriptions, "/v1/user/{user_id}/subscriptions")
swag.add_swag(Profile, "/v1/user/{user_id}/profile")
swag.add_swag(user.User, "/v1/org/{org_id}/module/{module_id}/user/{user_id}")
swag.add_swag(CheckEmail, "/v1/auth/email")
swag.add_swag(CheckUsername, "/v1/auth/username")
swag.add_swag(Register, "/v1/auth/register")
swag.add_swag(Login, "/v1/auth/login")
swag.add_swag(Verify2FA, "/v1/auth/2fa")
swag.add_swag(VerifyEmail, "/v1/auth/verify-email")
swag.add_swag(ConfirmEmail, "/v1/auth/confirm-email")

swag.start_swag()
print("Register swagger documentation")

# start app

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host="0.0.0.0")
