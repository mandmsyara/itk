import os


DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/wallet_db"
)


TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/wallet_test_db",
)
