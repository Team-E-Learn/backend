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
from backend.database.module_codes import ModuleCodesTable
from lib.dataswap.database import SwapDB
"""
Central module for database initialization and setup.
Coordinates the creation of all database tables and populates them with sample data.
Ensures proper order of operations to respect foreign key constraints during setup.
"""


# create all tables if they don't exist
def initialise_tables(conn: SwapDB) -> None:
    """Initialize all the database tables in the correct order.

    Creates all tables if they don't exist, ensuring proper sequencing
    to maintain foreign key integrity. Tables are created in an order
    that respects their dependencies (e.g. users' table before tables
    that reference user IDs).
    """
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
    ModuleCodesTable.create(conn)
    conn.commit()


# populate the tables with dummy data
def populate_dummy_data(conn: SwapDB) -> None:
    """
    Populate all tables with sample data for development and testing.

    Inserts sample records into each table, maintaining proper order to
    respect foreign key constraints. Each operation is committed separately
    to ensure database consistency between steps.

    This function supports development, testing, and demonstration purposes
    by creating a realistic dataset across all application entities.
    """
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
    ModuleCodesTable.write_codes(conn)
    conn.commit()
