from decouple import config

SECRET_KEY = config("EVENT_SECRET_KEY", cast=str)
ENV_ID = config("EVENT_ENV_ID", cast=str)