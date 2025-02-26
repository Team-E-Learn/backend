from psycopg.connection import Connection
from psycopg.rows import TupleRow

from backend.database.user import UserTable
from backend.database.email_codes import EmailCodesTable
from backend.database.organisations import OrganisationsTable
from backend.database.modules import ModulesTable
from backend.database.bundles import BundlesTable
from backend.database.bundles_modules import BundlesModulesTable
from backend.database.lessons import LessonsTable
from backend.database.blocks import BlocksTable
from backend.database.module_teachers import ModuleTeachersTable
from backend.database.subscriptions import SubscriptionsTable
from backend.database.dashboard import DashboardTable
from backend.database.module_dashboard import ModuleDashboardTable
from backend.database.progress import ProgressTable


# create all tables if they don't exist
def initialise_tables(conn: Connection[TupleRow]) -> None:
    UserTable.create(conn)
    EmailCodesTable.create(conn)
    OrganisationsTable.create(conn)
    ModulesTable.create(conn)
    BundlesTable.create(conn)
    BundlesModulesTable.create(conn)
    LessonsTable.create(conn)
    BlocksTable.create(conn)
    ModuleTeachersTable.create(conn)
    SubscriptionsTable.create(conn)
    DashboardTable.create(conn)
    ModuleDashboardTable.create(conn)
    ProgressTable.create(conn)
    conn.commit()


# populate the tables with dummy data
def populate_dummy_data(conn: Connection[TupleRow]) -> None:
    UserTable.write_users(conn)
    conn.commit()
    OrganisationsTable.write_orgs(conn)
    conn.commit()
    ModulesTable.write_modules(conn)
    conn.commit()
    BundlesTable.write_bundles(conn)
    conn.commit()
    LessonsTable.write_lessons(conn)
    conn.commit()
    BlocksTable.write_blocks(conn)
    conn.commit()
    SubscriptionsTable.write_subscriptions(conn)
    conn.commit()
    DashboardTable.write_dashboard(conn)
    conn.commit()
    ModuleDashboardTable.write_module_dashboard(conn)
    conn.commit()
