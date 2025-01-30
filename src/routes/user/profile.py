from flask_restful import Resource
from psycopg.connection import Connection
from psycopg.cursor import Cursor
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
    @Instil("db")
    def get(self, user_id: int, service: Connection[TupleRow]) -> dict[str, str]:
        # cursor: Cursor[TupleRow] = service.cursor()
        # _ = cursor.execute(
        #    """
        #    INSERT INTO users
        #    (accounttype, firstname, lastname, username, email)
        #    VALUES (
        #        'student', 'bob', 'example', 'bobbyexamples', 'bob@example.com'
        #    );
        # """
        # )
        # service.commit()
        return {"username": f"{user_id}"}
