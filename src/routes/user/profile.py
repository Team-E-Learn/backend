from flask_restful import Resource
from psycopg.connection import Connection
from psycopg.rows import TupleRow

from lib.instilled.instiled import Instil
from lib.swagdoc.swagdoc import SwagDoc, SwagMethod, SwagParam, SwagResp
from lib.swagdoc.swagmanager import SwagGen


class Profile(Resource):

    @SwagGen(
        SwagDoc(
            SwagMethod.GET,
            ["User"],
            "Returns the profile information for a specific user",
            [
                SwagParam(
                    "user_id",
                    "path",
                    "integer",
                    True,
                    "The user id to add to the module",
                    "1234",
                )
            ],
            [SwagResp(200, "Returns the profile information")],
        )
    )
    # gets the profile information for a user
    @Instil("db")
    def get(self, user_id: int, service: Connection[TupleRow]) -> dict[str, str]:
        with service.cursor() as cur:
            cur.execute(
                "SELECT username, email, firstName, lastName, accountType FROM users WHERE userID = %s",
                (user_id,)
            )
            user = cur.fetchone()
            if user:
                return {
                    "username": user[0],
                    "email": user[1],
                    "firstName": user[2],
                    "lastName": user[3],
                    "accountType": user[4]
                }
            else:
                return {"error": "User not found"}
