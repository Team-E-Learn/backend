#!/usr/bin/env python

from sys import stderr
from testing import run_tests
from flask.helpers import redirect
from flask_restful import Resource
from werkzeug.wrappers import Response

from backend.database.setup import initialise_tables, populate_dummy_data
from backend.events.logevent import LogEvent, LogLevel
from lib.dataswap.database import PsqlDatabase, SwapDB
from lib.front.front import Front
from lib.front.middleware import CORSMiddleware
from lib.instilled.instiled import Instil

from lib.metro.metro import MetroBus
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
from routes.module.lessons.block import Block
from routes.module.list_lessons import Lessons

from routes.user.dashboard.module import ModuleDashboard
from routes.user.dashboard.home import HomeDashboard

# Create Front facade for Flask
front: Front = Front(
    __name__,
    "Team Software Engineering Back-End API",
    "This API is for the prototype of a E-Learning platform that has been"
    + " developed for the Team Software Engineering module at the University of Lincoln.",
    "0.0.0",
)
front.add_middleware(CORSMiddleware())  # apply middleware for CORS


def log_event(event: LogEvent) -> None:
    """
    An event handler for LogEvents
    """
    if (
        event.level != LogLevel.LOG
    ):  # We don't need to log low level messages, this is for debug purposes
        return
    print(event, file=stderr)


MetroBus().subscribe(LogEvent, log_event)  # subscribe log_event to the event bus

# get Postgres connection
# conn: Connection[TupleRow] = psql_connect(projenv.DB_URL)
conn: SwapDB = PsqlDatabase(projenv.DB_URL)
print("Database connected")

# Initialise tables for project
initialise_tables(conn)  # Create tables if they don't exist
print("Initialized tables")

# Add database service for Instil
Instil.add_service("db", conn)
print("Registered database service")


class Main(Resource):

    def get(self) -> Response:
        _ = MetroBus().publish(LogEvent(LogLevel.LOG, "Accessed docs."))
        return redirect("/apidocs")


# Register main route
front.register(Main, "/", docs=False)

# Register routes
front.add_tag(SwagTag("Organisation", "Organisation related endpoints"))
front.add_tag(SwagTag("Module", "Module related endpoints"))
front.add_tag(SwagTag("User", "User related endpoints"))
front.register(Subscriptions, "/v1/user/<int:user_id>/subscriptions")
front.register(Profile, "/v1/user/<int:user_id>/profile")
front.register(User, "/v1/org/<int:org_id>/module/<int:module_id>/user/<int:user_id>")
front.register(CheckEmail, "/v1/auth/email")
front.register(CheckUsername, "/v1/auth/username")
front.register(Register, "/v1/auth/register")
front.register(Login, "/v1/auth/login")
front.register(Verify2FA, "/v1/auth/2fa")
front.register(VerifyEmail, "/v1/auth/verify-email")
front.register(Lessons, "/v1/module/<int:module_id>/lessons")
front.register(Lesson, "/v1/module/lesson/")
front.register(Block, "/v1/module/lesson/<int:lesson_id>/block")
front.register(HomeDashboard, "/v1/user/<int:user_id>/dashboard")
front.register(
    ModuleDashboard, "/v1/user/<int:user_id>/dashboard/module/<int:module_id>"
)


# Start app
if __name__ == "__main__":
    debug_mode: bool = projenv.project_mode == projenv.ProjectMode.DEVELOPMENT
    if debug_mode:
        # Write dummy data
        populate_dummy_data(conn)
        # Run tests
        #run_tests(conn)

    front.start(debug=debug_mode)
