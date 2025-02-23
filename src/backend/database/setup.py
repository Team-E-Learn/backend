from psycopg.connection import Connection
from psycopg.rows import TupleRow

from backend.database.bundles import BundlesTable
from backend.database.bundles_modules import BundlesModulesTable
from backend.database.module_teachers import ModuleTeachersTable
from backend.database.modules import ModulesTable
from backend.database.organisations import OrganisationsTable
from backend.database.progress import ProgressTable
from backend.database.subscriptions import SubscriptionsTable
from backend.database.user import UserTable
from backend.database.blocks import BlocksTable
from backend.database.lessons import LessonsTable


def initialise_tables(conn: Connection[TupleRow]) -> None:
    UserTable.create(conn)
    OrganisationsTable.create(conn)
    ModulesTable.create(conn)
    BundlesTable.create(conn)
    BundlesModulesTable.create(conn)
    LessonsTable.create(conn)
    BlocksTable.create(conn)
    ModuleTeachersTable.create(conn)
    ProgressTable.create(conn)
    SubscriptionsTable.create(conn)
    conn.commit()
