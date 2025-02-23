from psycopg.connection import Connection
from psycopg.rows import TupleRow

from backend.database.user import UserTable
from backend.database.organisations import OrganisationsTable
from backend.database.modules import ModulesTable
from backend.database.bundles import BundlesTable
from backend.database.bundles_modules import BundlesModulesTable
from backend.database.lessons import LessonsTable
from backend.database.blocks import BlocksTable
from backend.database.module_teachers import ModuleTeachersTable
from backend.database.subscriptions import SubscriptionsTable
from backend.database.progress import ProgressTable

# create all tables if they don't exist
def initialise_tables(conn: Connection[TupleRow]) -> None:
    UserTable.create(conn)
    OrganisationsTable.create(conn)
    ModulesTable.create(conn)
    BundlesTable.create(conn)
    BundlesModulesTable.create(conn)
    LessonsTable.create(conn)
    BlocksTable.create(conn)
    ModuleTeachersTable.create(conn)
    SubscriptionsTable.create(conn)
    ProgressTable.create(conn)
    conn.commit()
