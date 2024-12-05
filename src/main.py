#!/usr/bin/env python
# setup and initialize flask app

import profile
from flask import Flask, redirect
from flask_restful import Api, Resource
from flasgger import Swagger
from werkzeug.wrappers import Response

from routes.user import subscriptions
from routes.org.module import user

# start flask app

app: Flask = Flask(__name__)
api: Api = Api(app)
swagger = Swagger(app, template={
    "info": {
        "title": "Python TSE backend API",
        "description": "Examples of how to use the projects python API",
        "version": "0.0.0"
    },

    "tags": [
        {"name": "Stock info", "description": "Information on a specific stock(s)"},
        {"name": "Market info", "description": "Information on specific markets and/or indexes"},
    ],


    "paths": {
    }
})

class Main(Resource):
    def get(self) -> Response:
        return redirect("/apidocs")

api.add_resource(Main, "/")
api.add_resource(subscriptions.Subscriptions, "/v1/user/<int:user_id>/subscriptions")
api.add_resource(profile.Profile, "/v1/user/<int:user_id>/profile")
api.add_resource(user.User, "/v1/org/<int:org_id>/module/<int:module_id>/user/<int:user_id>")

# start app

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0')







