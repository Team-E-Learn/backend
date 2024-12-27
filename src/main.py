#!/usr/bin/env python
# setup and initialize flask app
# setup and initialize postgresql database

from flask import Flask, redirect
from flask_restful import Api, Resource
from werkzeug.wrappers import Response

from lib.swagdoc.swagmanager import SwagManager
from lib.swagdoc.swagtag import SwagTag
from routes.user import subscriptions, profile
from routes.org.module import user
import psycopg

# start postgresql database

# password is whatever you set it to be when you installed postgresql
db = psycopg.connect("dbname=dev user=postgres password=class")
print("Database connected")

# if tables do not exist, create them

cur = db.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        userID SERIAL PRIMARY KEY UNIQUE NOT NULL,
        accountType VARCHAR(16) NOT NULL,
        firstName VARCHAR(48) NOT NULL,
        lastName VARCHAR(48) NOT NULL,
        username VARCHAR(64) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL
    );
    CREATE TABLE IF NOT EXISTS organisations (
        orgID SERIAL PRIMARY KEY UNIQUE NOT NULL,
        name VARCHAR(48) UNIQUE NOT NULL,
        description VARCHAR(100) NOT NULL,
        ownerID INT REFERENCES users(userID) NOT NULL
    );
    CREATE TABLE IF NOT EXISTS modules (
        moduleID SERIAL PRIMARY KEY UNIQUE NOT NULL,
        name VARCHAR(48) NOT NULL,
        description VARCHAR(100) NOT NULL,
        orgID INT REFERENCES organisations(orgID) NOT NULL
    );
    CREATE TABLE IF NOT EXISTS module_teachers (
        moduleID INT REFERENCES modules(moduleID) NOT NULL,
        userID INT REFERENCES users(userID) NOT NULL,
        PRIMARY KEY (moduleID, userID)
    );
    CREATE TABLE IF NOT EXISTS bundles (
        bundleID SERIAL PRIMARY KEY UNIQUE NOT NULL,
        name VARCHAR(48) NOT NULL,
        description VARCHAR(100) NOT NULL,
        orgID INT REFERENCES organisations(orgID) NOT NULL
    );
    CREATE TABLE IF NOT EXISTS bundle_modules (
        bundleID INT REFERENCES bundles(bundleID) NOT NULL,
        moduleID INT REFERENCES modules(moduleID) NOT NULL,
        PRIMARY KEY (bundleID, moduleID)
    );
    CREATE TABLE IF NOT EXISTS content (
        contentID SERIAL PRIMARY KEY UNIQUE NOT NULL,
        moduleID INT REFERENCES modules(moduleID) NOT NULL,
        title VARCHAR(48) NOT NULL,
        description VARCHAR(100) NOT NULL,
        content JSON NOT NULL
    );
    CREATE TABLE IF NOT EXISTS subscriptions (
        userID INT REFERENCES users(userID) NOT NULL,
        moduleID INT REFERENCES modules(moduleID) NOT NULL,
        PRIMARY KEY (userID, moduleID)
    );
    CREATE TABLE IF NOT EXISTS progress (
        userID INT REFERENCES users(userID) NOT NULL,
        moduleID INT REFERENCES modules(moduleID) NOT NULL,
        progress JSON NOT NULL
    );
""")
db.commit()


# start flask app

app: Flask = Flask(__name__)
api: Api = Api(app)
swag: SwagManager = SwagManager(
    app,
    "Python TSE backend API",
    "Examples of how to use the projects python API",
    "0.0.0",
)


class Main(Resource):

    def get(self) -> Response:
        return redirect("/apidocs")


api.add_resource(Main, "/")
api.add_resource(subscriptions.Subscriptions, "/v1/user/<int:user_id>/subscriptions")
api.add_resource(profile.Profile, "/v1/user/<int:user_id>/profile")
api.add_resource(user.User, "/v1/org/<int:org_id>/module/<int:module_id>/user/<int:user_id>")

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