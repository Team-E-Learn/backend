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
from routes.user import subscriptions, profile
from routes.org.module import user

# start flask app

app: Flask = Flask(__name__)
api: Api = Api(app)
swag: SwagManager = SwagManager(
    app,
    "Python TSE backend API",
    "Examples of how to use the projects python API",
    "0.0.0",
)

conn: Connection[TupleRow] = psql_connect(
    "postgresql://postgres:cisco@127.0.0.1:5432/dev"
)
print("Database connected")
initialise_tables(conn)  # create tables if they don't exist
# TODO: initialise some data into the tables


Instil.add_service("db", conn)


class Main(Resource):

    def get(self) -> Response:
        return redirect("/apidocs")


api.add_resource(Main, "/")
api.add_resource(subscriptions.Subscriptions, "/v1/user/<int:user_id>/subscriptions")
api.add_resource(profile.Profile, "/v1/user/<int:user_id>/profile")
api.add_resource(
    user.User, "/v1/org/<int:org_id>/module/<int:module_id>/user/<int:user_id>"
)

swag.add_tag(SwagTag("Organisation", "Organisation related endpoints"))
swag.add_tag(SwagTag("Module", "Module related endpoints"))
swag.add_tag(SwagTag("User", "User related endpoints"))
swag.add_swag(subscriptions.Subscriptions, "/v1/user/<user_id>/subscriptions")
swag.add_swag(profile.Profile, "/v1/user/<user_id>/profile")
swag.add_swag(user.User, "/v1/org/<org_id>/module/<module_id>/user/<user_id>")

swag.start_swag()

# start app

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host="0.0.0.0")
