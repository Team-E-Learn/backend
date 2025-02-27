#!/usr/bin/env python

from flask import Flask, redirect
from flask_restful import Api, Resource
from psycopg.connection import Connection
from psycopg.rows import TupleRow
from psycopg import connect as psql_connect
from werkzeug.wrappers import Response

from backend.database.setup import initialise_tables, populate_dummy_data
from lib.front.front import Front
from lib.instilled.instiled import Instil

from lib.swagdoc.swagmanager import SwagManager
from lib.swagdoc.swagtag import SwagTag
from routes.auth.email import CheckEmail
from routes.auth.register import Register
from routes.auth.username import CheckUsername
from routes.auth.verify_email import VerifyEmail
from routes.user.profile import Profile
from routes.user.subscriptions import Subscriptions
from routes.org.module.user import User
from routes.auth.login import Login
from routes.auth.verify2fa import Verify2FA

import projenv
from routes.module.lessons.lesson import Lesson
from routes.module.list_lessons import Lessons

from routes.user.dashboard.module import ModuleDashboard
from routes.user.dashboard.home import HomeDashboard

app: Flask = Flask(__name__)
front: Front = Front(app)


@app.after_request
def after_request(response: Response) -> Response:
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    return response


conn: Connection[TupleRow] = psql_connect(projenv.DB_URL)
print("Database connected")
initialise_tables(conn)  # create tables if they don't exist
print("Initialized tables")

Instil.add_service("db", conn)
print("Registered database service")


class Main(Resource):

    def get(self) -> Response:
        return redirect("/apidocs")


front.add_resource(Main, "/")

front.add_swag_tag(SwagTag("Organisation", "Organisation related endpoints"))
front.add_swag_tag(SwagTag("Module", "Module related endpoints"))
front.add_swag_tag(SwagTag("User", "User related endpoints"))

front.register(
    Subscriptions,
    "/v1/user/<int:user_id>/subscriptions",
    "/v1/user/{user_id}/subscriptions",
)
front.register(Profile, "/v1/user/<int:user_id>/profile", "/v1/user/{user_id}/profile")
front.register(
    User,
    "/v1/org/<int:org_id>/module/<int:module_id>/user/<int:user_id>",
    "/v1/org/{org_id}/module/{module_id}/user/{user_id}",
)
front.register(CheckEmail, "/v1/auth/email", "/v1/auth/email")
front.register(CheckUsername, "/v1/auth/username", "/v1/auth/username")
front.register(Register, "/v1/auth/register", "/v1/auth/register")
front.register(Login, "/v1/auth/login", "/v1/auth/login")
front.register(Verify2FA, "/v1/auth/2fa", "/v1/auth/2fa")
front.register(VerifyEmail, "/v1/auth/verify-email", "/v1/auth/verify-email")
front.register(
    Lessons,
    "/v1/module/<int:module_id>/lessons",
    "/v1/module/{module_id}/lessons",
)
front.register(
    Lesson,
    "/v1/module/lesson/<int:lesson_id>",
    "/v1/module/lesson/{lesson_id}",
)
front.register(
    HomeDashboard,
    "/v1/user/<int:user_id>/dashboard",
    "/v1/user/{user_id}/dashboard",
)
front.register(
    ModuleDashboard,
    "/v1/user/<int:user_id>/dashboard/module/<int:module_id>",
    "/v1/user/{user_id}/dashboard/module/{module_id}",
)


front.start()
print("Register swagger documentation")

# write dummy data
populate_dummy_data(conn)

# start app

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host="0.0.0.0")
