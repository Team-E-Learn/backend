from flask_restful import Resource
from psycopg.connection import Connection
from psycopg.rows import TupleRow

from lib.instilled.instiled import Instil
from lib.swagdoc.swagdoc import SwagDoc, SwagParam, SwagMethod, SwagResp
from lib.swagdoc.swagmanager import SwagGen


class User(Resource):

    @SwagGen(
        SwagDoc(
            SwagMethod.PUT,
            ["Module"],
            "Adds a bundle or module to a user",
            [
                SwagParam(
                    "org_id",
                    "path",
                    "integer",
                    True,
                    "The org id to add the module to",
                    "1",
                ),
                SwagParam(
                    "module_id",
                    "path",
                    "integer",
                    True,
                    "The module id to add the user to",
                    "1",
                ),
                SwagParam(
                    "user_id",
                    "path",
                    "integer",
                    True,
                    "The user id to add to the module",
                    "1",
                ),
            ],
            [SwagResp(200, "Module added to user")],
        )
    )

    @Instil('db')
    def put(self, org_id: int, module_id: int, user_id: int, service: Connection[TupleRow]) -> dict[str, bool]:
        with service.cursor() as cur:
            # check user_id exists in the users table
            cur.execute("SELECT 1 FROM users WHERE userID = %s", (user_id,))
            if cur.fetchone() is None:
                return {"success": False, "error": "User not found"}

            # check org_id exists
            cur.execute("SELECT 1 FROM organisations WHERE orgID = %s", (org_id,))
            if cur.fetchone() is None:
                return {"success": False, "error": "Organisation not found"}

            # check module_id exists
            cur.execute("SELECT 1 FROM modules WHERE moduleID = %s", (module_id,))
            if cur.fetchone() is None:
                return {"success": False, "error": "Module not found"}

            # check org owns module
            cur.execute("SELECT 1 FROM modules WHERE moduleID = %s AND orgID = %s", (module_id, org_id))
            if cur.fetchone() is None:
                return {"success": False, "error": "Organisation does not own the module"}

            # insert into subscriptions user_id and module_id
            try:
                cur.execute("INSERT INTO subscriptions (userID, moduleID) VALUES (%s, %s)",
                    (user_id, module_id)
                )
                service.commit()
                return {"success": True}
            except Exception as e:
                return {"success": False, "error": str(e)}



