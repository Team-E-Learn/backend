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
from routes.user import subscriptions, profile
from routes.org.module import user
from routes.auth import login, register, verify2fa

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
api.add_resource(subscriptions.Subscriptions, "/v1/user/<int:user_id>/subscriptions")
api.add_resource(profile.Profile, "/v1/user/<int:user_id>/profile")
api.add_resource(
    user.User, "/v1/org/<int:org_id>/module/<int:module_id>/user/<int:user_id>")
api.add_resource(login.Login, "/v1/auth/login")
api.add_resource(register.RegisterEmail, "/v1/auth/email")
api.add_resource(register.VerifyEmail, "/v1/auth/verifyEmail")
api.add_resource(register.Username, "/v1/auth/username")
api.add_resource(register.Password, "/v1/auth/password")
api.add_resource(verify2fa.Verify2FA, "/v1/auth/verify2fa")


swag.add_tag(SwagTag("Organisation", "Organisation related endpoints"))
swag.add_tag(SwagTag("Module", "Module related endpoints"))
swag.add_tag(SwagTag("User", "User related endpoints"))
swag.add_swag(subscriptions.Subscriptions, "/v1/user/{user_id}/subscriptions")
swag.add_swag(profile.Profile, "/v1/user/{user_id}/profile")
swag.add_swag(user.User, "/v1/org/{org_id}/module/{module_id}/user/{user_id}")
swag.add_swag(login.Login, "/v1/auth/login")
swag.add_swag(register.RegisterEmail, "/v1/auth/email")
swag.add_swag(register.VerifyEmail, "/v1/auth/verifyEmail")
swag.add_swag(register.Username, "/v1/auth/username")
swag.add_swag(register.Password, "/v1/auth/password")
swag.add_swag(verify2fa.Verify2FA, "/v1/auth/verify2fa")

swag.start_swag()
print("Register swagger documentation")

# start app

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host="0.0.0.0")
