# setup and initialize flask app

from flask import Flask, redirect
from flask_restful import Api
from flasgger import Swagger
from werkzeug.wrappers import Response

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
        "/tns/{company_name}": {
            "get": {
                "tags": ["Stock info"],
                "summary": "Attempts to find and return the ticker symbol for a specific company",#
                "parameters": [
                    {    "name": "company_name",
                        "in": "path",
                        "type": "string",
                        "required": True,
                        "description": "The name of the company to get the ticker symbol for",
                        "default": "Nvidia"
                    }
                ],
                "responses": {"200": {"description": "Returns the ticker symbol"}}
            }
        },
    }
})

@app.get("/")
def main() -> Response:
    return redirect("/apidocs") 


# start app

if __name__ == '__main__':
    app.run(debug=True)






