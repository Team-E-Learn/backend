from psycopg.connection import Connection
from psycopg.rows import TupleRow

from bundles import BundlesTable
from bundles_modules import BundlesModulesTable
from content import ContentTable
from module_teachers import ModuleTeachersTable
from modules import ModulesTable
from organisations import OrganisationsTable
from progress import ProgressTable
from subscriptions import SubscriptionsTable
from user import UserTable


def initialise_tables(conn: Connection[TupleRow]) -> None:
    BundlesTable.create(conn)
    BundlesModulesTable.create(conn)
    ContentTable.create(conn)
    ModuleTeachersTable.create(conn)
    ModulesTable.create(conn)
    OrganisationsTable.create(conn)
    ProgressTable.create(conn)
    SubscriptionsTable.create(conn)
    UserTable.create(conn)
