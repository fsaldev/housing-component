from os import getenv
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

AUTO_RELOAD = getenv("AUTO_RELOAD", "0") != "0"

LOGGING_LEVEL = getenv("LOGGING_LEVEL", "DEBUG")
LOGGING_PATH = getenv("LOGGING_PATH", None)
LOGGING_JSON = getenv("LOGGING_JSON", "0") != "0"
LOGGING_PREFIX = getenv("LOGGING_PREFIX", "hm:")

DB_USERNAME = getenv("DB_USERNAME", "postgres")
DB_PASSWORD = getenv("DB_PASSWORD", "postgres")
DB_HOST = getenv("DB_HOST", "localhost")
DB_PORT = int(getenv("DB_PORT", 5436))
DB_NAME = getenv("DB_NAME", "housing_component")
DB_ECHO = getenv("DB_ECHO", "0") != "0"
DB_URL = (
    f"postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

AMQP_BROKER_HOST = getenv("AMQP_BROKER_HOST", "localhost")
AMQP_BROKER_PORT = int(getenv("AMQP_BROKER_PORT", 5672))
AMQP_BROKER_USERNAME = getenv("AMQP_BROKER_USERNAME", "guest")
AMQP_BROKER_PASSWORD = getenv("AMQP_BROKER_PASSWORD", "guest")
AMQP_BROKER_VIRTUAL_HOST = getenv("AMQP_BROKER_VIRTUAL_HOST", "/")
AMQP_EXCHANGE_NAME = getenv("AMQP_EXCHANGE_NAME", "events")
AMQP_CONSUMER_QUEUE_NAME = getenv(
    "AMQP_CONSUMER_QUEUE_NAME", "housing-component.events.subscriptions"
)
AMQP_PREFETCH_COUNT = int(getenv("AMQP_PREFETCH_COUNT", 1))

ACCESS_TOKEN_SECRET_KEY = getenv("ACCESS_TOKEN_SECRET_KEY", "")
ACCESS_TOKEN_ALGORITHM = getenv("ACCESS_TOKEN_ALGORITHM", "HS256")
ACCESS_TOKEN_ISSUER = getenv("ACCESS_TOKEN_ISSUER", "https://api.kiwi.ki")
ACCESS_TOKEN_AUDIENCE = getenv("ACCESS_TOKEN_AUDIENCE", "https://housing.kiwi.ki")
ACCESS_TOKEN_LEEWAY = int(getenv("ACCESS_TOKEN_LEEWAY", 10))
SENSOR_URL = f"{ACCESS_TOKEN_ISSUER}/pre/sensors"
CREATE_USER_URL = f"{ACCESS_TOKEN_ISSUER}/pre/users"
FETCH_USER_URL = f"{ACCESS_TOKEN_ISSUER}/pre/users/username"
GRANT_PERMISSIONS_URL = f"{ACCESS_TOKEN_ISSUER}/pre/permissions/user/sensor"
KIWI_USERNAME = getenv("KIWI_USERNAME", "kiwikigmbh")
KIWI_PASSWORD = getenv("KIWI_PASSWORD", "password123")
SESSION_URL = f"{ACCESS_TOKEN_ISSUER}/pre/session"
REMOVE_PERMISSION_URL = f"{ACCESS_TOKEN_ISSUER}/pre/permissions/"
