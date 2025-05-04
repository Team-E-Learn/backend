from flask_restful import Resource

from backend.database.modules import ModulesTable
from lib.dataswap.database import SwapDB
from lib.instilled.instiled import Instil
from lib.swagdoc.swagdoc import SwagDoc, SwagMethod, SwagParam, SwagResp
from lib.swagdoc.swagmanager import SwagGen


class Module(Resource):
    @SwagGen(
        SwagDoc(
            SwagMethod.GET,
            ["Module"],
            "Returns the information associated with a given module",
            [
                SwagParam(
                    "module_id",
                    "path",
                    "integer",
                    True,
                    "The module id to retrieve the information for",
                    "1",
                )
            ],
            [
                SwagResp(200, "Returns the lessons"),
                SwagResp(404, "Could not find the lesson"),
            ],
        )
    )
    @Instil("db")
    def get(self, module_id: int, service: SwapDB):
        module: tuple[int, str, str, int] | None = ModulesTable.get_info(
            service, module_id
        )

        if module is None:
            return {"error": "Module not found"}, 404

        return {
            "module_id": module[0],
            "name": module[1],
            "description": module[2],
            "org_id": module[3],
        }, 200
