#!/usr/bin/env python

from flask import Flask, redirect
from flask_restful import Api, Resource
from psycopg.connection import Connection
from psycopg.rows import TupleRow
from psycopg import connect as psql_connect
from werkzeug.wrappers import Response

from backend.database.setup import initialise_tables
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
from routes.course.lessons.lesson import Lesson
from routes.course.lessons_ import Lessons

from routes.user.dashboard.course import CourseDashboard
from routes.user.dashboard.home import HomeDashboard

app: Flask = Flask(__name__)
api: Api = Api(app)
swag: SwagManager = SwagManager(
    app,
    "Python TSE backend API",
    "Examples of how to use the projects python API",
    "0.0.0",
)


conn: Connection[TupleRow] = psql_connect(projenv.DB_URL)
print("Database connected")
initialise_tables(conn)  # create tables if they don't exist
print("Initialized tables")

Instil.add_service("db", conn)
print("Registered database service")


class Main(Resource):

    def get(self) -> Response:
        return redirect("/apidocs")


def register(
    resource: type[Resource],
    route: str,
    swag_route: str,
    swag_manager: SwagManager,
    api: Api,
) -> None:
    api.add_resource(resource, route)
    swag_manager.add_swag(resource, swag_route)


api.add_resource(Main, "/")

swag.add_tag(SwagTag("Organisation", "Organisation related endpoints"))
swag.add_tag(SwagTag("Module", "Module related endpoints"))
swag.add_tag(SwagTag("User", "User related endpoints"))

register(
    Subscriptions,
    "/v1/user/<int:user_id>/subscriptions",
    "/v1/user/{user_id}/subscriptions",
    swag,
    api,
)

register(
    Profile, "/v1/user/<int:user_id>/profile", "/v1/user/{user_id}/profile", swag, api
)

register(
    User,
    "/v1/org/<int:org_id>/module/<int:module_id>/user/<int:user_id>",
    "/v1/org/{org_id}/module/{module_id}/user/{user_id}",
    swag,
    api,
)

register(CheckEmail, "/v1/auth/email", "/v1/auth/email", swag, api)
register(CheckUsername, "/v1/auth/username", "/v1/auth/username", swag, api)
register(Register, "/v1/auth/register", "/v1/auth/register", swag, api)
register(Login, "/v1/auth/login", "/v1/auth/login", swag, api)
register(Verify2FA, "/v1/auth/2fa", "/v1/auth/2fa", swag, api)
register(VerifyEmail, "/v1/auth/verify-email", "/v1/auth/verify-email", swag, api)
register(Lessons, "/v1/course/lessons", "/v1/course/lessons", swag, api)
register(
    Lesson,
    "/v1/course/lesson/<int:lesson_id>",
    "/v1/course/lesson/{lesson_id}",
    swag,
    api,
)
register(HomeDashboard, "/v1/user/dashboard/home", "/v1/user/dashboard/home", swag, api)
register(
    CourseDashboard, "/v1/user/dashboard/course", "/v1/user/dashboard/course", swag, api
)


swag.start_swag()
print("Register swagger documentation")

# start app

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host="0.0.0.0")
