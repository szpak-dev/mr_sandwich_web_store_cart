from os import getenv

settings = {
    'APP_LOG_LEVEL': getenv('APP_LOG_LEVEL', 'DEBUG'),
    'DATABASE_DSN': getenv('DATABASE_DSN', 'postgresql+asyncpg://postgres:postgres@localhost:5435/web_store_cart'),
    'RABBITMQ_DSN': getenv('RABBITMQ_DSN', 'amqp://guest:guest@localhost:5672/'),
    'FOOD_FACTORY_URL': getenv('FOOD_FACTORY_URL', 'http://127.0.0.1:8001'),
}
