import os
import uuid


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", str(uuid.uuid4()))
    POSTGRES = {
        "user": os.getenv("POSTGRES_USER", "postgres"),
        "pw": os.getenv("POSTGRES_PASSWORD", "postgres"),
        "db": os.getenv("POSTGRES_DB", "malerpris"),
        "host": os.getenv("POSTGRES_HOST", "127.0.0.1"),
        "port": os.getenv("POSTGRES_PORT", "5432")
    }
    SQLALCHEMY_DATABASE_URI = "postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s" % POSTGRES
    BABEL_DEFAULT_LOCALE = 'da'
