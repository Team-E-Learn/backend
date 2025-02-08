# Temporary solution for storing environment variables

"""
Database Access
"""
DB_UNAME: str = "postgres"
DB_PWD: str = "cisco"
DB_HOSTNAME: str = "localhost"
DB_PORT: str = "5432"
DB_NAME: str = "dev"

DB_URL: str = f"postgresql://{DB_UNAME}:{DB_PWD}@{DB_HOSTNAME}:{DB_PORT}/{DB_NAME}"


"""
JWT Signing Keys
"""

# token for limited usage until 2fa used
JWT_LOGIN_KEY: bytes = b"secretkey"
JWT_LOGIN_EXP: int = 1_800  # seconds
