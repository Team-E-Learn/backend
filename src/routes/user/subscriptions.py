from typing import Any

from flask_restful import Resource
from psycopg.connection import Connection
from psycopg.rows import TupleRow

from lib.instilled.instiled import Instil
from lib.swagdoc.swagdoc import SwagDoc, SwagMethod, SwagParam, SwagResp
from lib.swagdoc.swagmanager import SwagGen


class Subscriptions(Resource):
    
    @SwagGen(
        SwagDoc(
            SwagMethod.GET,
            ["User"],
            "Returns the subscribed orgs, bundles and modules for a user",
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
            [SwagResp(200, "Returns the subscriptions")],
        )
    )

    @Instil('db')
    def get(self, user_id: int, service: Connection[TupleRow]) -> list[dict[str, Any]]:
        # get the user's subscriptions
        with service.cursor() as cur:
            cur.execute("""
                SELECT organisations.orgID, organisations.name AS orgName,
                       bundles.bundleID, bundles.name AS bundleName,
                       modules.moduleID, modules.name AS moduleName
                FROM subscriptions
                JOIN modules ON subscriptions.moduleID = modules.moduleID
                LEFT JOIN bundle_modules ON modules.moduleID = bundle_modules.moduleID
                LEFT JOIN bundles ON bundle_modules.bundleID = bundles.bundleID
                JOIN organisations ON modules.orgID = organisations.orgID
                WHERE subscriptions.userID = %s
            """, (user_id,))
            subscriptions = cur.fetchall()

            # convert the subscriptions into a more readable format
            orgs = []
            for org_id, org_name, bundle_id, bundle_name, module_id, module_name in subscriptions:
                # check if the org is already in the list
                org = next((org for org in orgs if org["org_id"] == org_id), None)
                if org is None:
                    org = {
                        "org_name": org_name,
                        "org_id": org_id,
                        "bundles": [],
                        "modules": []
                    }
                    orgs.append(org)

                if bundle_id:
                    # check if the bundle is already in the list
                    bundle = next((b for b in org["bundles"] if b["bundle_id"] == bundle_id), None)
                    if bundle is None:
                        bundle = {
                            "bundle_id": bundle_id,
                            "bundle_name": module_name,  # use module_name as bundle_name
                            "modules": []
                        }
                        org["bundles"].append(bundle)

                    # add module to the bundle
                    bundle["modules"].append({
                        "name": bundle_name,  # use bundle_name as module_name
                        "module_id": module_id
                    })
                else:
                    # add module directly to the orgs modules list
                    org["modules"].append({
                        "name": module_name,
                        "module_id": module_id
                    })

        return orgs