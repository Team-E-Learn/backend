from dataclasses import dataclass
from typing import Any, TypeAlias
from flask_restful import Resource
from backend.auth import valid_jwt_sub
from lib.dataswap.cursor import SwapCursor
from lib.dataswap.database import SwapDB
from lib.dataswap.result import SwapResult
from lib.dataswap.statement import StringStatement
from lib.instilled.instiled import Instil
from lib.swagdoc.swagdoc import SwagDoc, SwagMethod, SwagParam, SwagResp
from lib.swagdoc.swagmanager import SwagGen


ModuleJson: TypeAlias = dict[str, str | int]
BundleJson: TypeAlias = dict[str, str | int | list[ModuleJson]]
OrgJson: TypeAlias = dict[str, str | int | list[ModuleJson] | list[BundleJson]]


@dataclass
class Module:
    module_id: int
    module_name: str

    def to_dict(self) -> ModuleJson:
        return {"name": self.module_name, "module_id": self.module_id}


@dataclass
class Bundle:
    bundle_id: int
    bundle_name: str
    modules: list[Module]

    def to_dict(self) -> BundleJson:
        return {
            "bundle_id": self.bundle_id,
            "bundle_name": self.bundle_name,
            "modules": [mod.to_dict() for mod in self.modules],
        }


@dataclass
class Org:
    org_id: int
    org_name: str
    bundles: list[Bundle]
    modules: list[Module]

    def to_dict(self) -> OrgJson:
        return {
            "org_name": self.org_name,
            "org_id": self.org_id,
            "bundles": [bund.to_dict() for bund in self.bundles],
            "modules": [mod.to_dict() for mod in self.modules],
        }


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
                    "The user id get the subscriptions for",
                    "3",
                )
            ],
            [SwagResp(200, "Returns the subscriptions")],
            protected=True
        )
    )
    @Instil("db")
    def get(self, user_id: int, service: SwapDB) -> [list[OrgJson], int]:
        # Get the user's subscriptions
        if not valid_jwt_sub(user_id):
            return {"message": "You are unauthorised to access this endpoint"}, 401

        cur: SwapCursor = service.get_cursor()
        result: SwapResult = cur.execute(
            StringStatement(
                """
            SELECT organisations.orgID, organisations.name AS orgName,
                   bundles.bundleID, bundles.name AS bundleName,
                   modules.moduleID, modules.name AS moduleName
            FROM subscriptions
            JOIN modules ON subscriptions.moduleID = modules.moduleID
            LEFT JOIN bundle_modules ON modules.moduleID = bundle_modules.moduleID
            LEFT JOIN bundles ON bundle_modules.bundleID = bundles.bundleID
            JOIN organisations ON modules.orgID = organisations.orgID
            WHERE subscriptions.userID = %s
        """
            ),
            (user_id,),
        )
        subscriptions: list[tuple[Any, ...]] | None = result.fetch_all()

        if subscriptions is None or len(subscriptions) == 0:
            return []

        # Convert the subscriptions into a more readable format
        orgs: list[Org] = []
        for sub in subscriptions:
            org_id: int = sub[0]
            org_name: str = sub[1]
            bundle_id: int | None = sub[2]
            bundle_name: str | None = sub[3]
            module_id: int = sub[4]
            module_name: str = sub[5]

            # Check if the org is already in the list
            org: Org | None = next((org for org in orgs if org.org_id == org_id), None)

            # If the org is not in the list, add it
            if org is None:
                org = Org(org_id, org_name, [], [])
                orgs.append(org)

            # Check if the module is a standalone module
            if bundle_id is None or bundle_name is None:
                # Add module directly to the orgs modules list
                org.modules.append(Module(module_id, module_name))
                continue

            # Check if the bundle is already in the list
            bundle: Bundle | None = next(
                (bundle for bundle in org.bundles if bundle.bundle_id == bundle_id),
                None,
            )

            # If the bundle is not in the list, add it
            if bundle is None:
                bundle = Bundle(bundle_id, bundle_name, [])
                org.bundles.append(bundle)

            # Add module to the bundle
            bundle.modules.append(Module(module_id, module_name))

        # Convert the orgs list to a list of dictionaries
        return [org.to_dict() for org in orgs], 200
