# Temporary solution for storing environment variables

from enum import Enum


class ProjectMode(Enum):
    DEVELOPMENT = 0
    PRODUCTION = 1


"""
Project Mode
"""
project_mode: ProjectMode = ProjectMode.DEVELOPMENT

"""
Database Access
"""
DB_UNAME: str = "postgres"
DB_PWD: str = "cisco"
#DB_HOSTNAME: str = "postgres"
DB_HOSTNAME: str = "127.0.0.1"
DB_PORT: str = "5432"
DB_NAME: str = "dev"

DB_URL: str = f"postgresql://{DB_UNAME}:{DB_PWD}@{DB_HOSTNAME}:{DB_PORT}/{DB_NAME}"


"""
JWT Signing Keys
"""

# token for limited usage until 2fa used
JWT_LIMITED_KEY: bytes = b"secretkeysecretkeysecretkeysecretkey"
JWT_LIMITED_EXP: int = 1_800  # seconds

# token for full access
JWT_ACCESS_KEY: bytes = b"secretkeysecretkeysecretkeysecretkey"
JWT_ACCESS_EXP: int = 36_000  # seconds


"""
Email Sending Token
"""

EMAIL_API_TOKEN: str = (
    "TVL7fjlHixxphDqrAmzTbNgKAMqbJivLjZ8d6CpYCExQIVMAadBDG3uyXyEqv4t74b0yE8"
)
