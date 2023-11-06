import os
import peewee
from contextvars import ContextVar
from fastapi import Depends


DB_NAME = os.environ.get("DB_DBNAME") if os.environ.get("DB_DBNAME") else "airflow"
DB_HOST = os.environ.get("DB_HOST") if os.environ.get("DB_HOST") else "localhost"
DB_PORT =os.environ.get("DB_PORT") if os.environ.get("DB_PORT") else 5432
DB_USER = os.environ.get("DB_USER") if os.environ.get("DB_USER") else "opponent"
DB_PASSWORD = os.environ.get("DB_PASSWORD") if os.environ.get("DB_HOST") else "opponent"
DB_SCHEMA = os.environ.get("DB_SCHEMA") if os.environ.get("DB_SCHEMA") else "test"


db_state_default = {"closed": None, "conn": None, "ctx": None, "transactions": None}
db_state = ContextVar("db_state", default=db_state_default.copy())

class PeeweeConnectionState(peewee._ConnectionState):
    def __init__(self, **kwargs):
        super().__setattr__("_state", db_state)
        super().__init__(**kwargs)

    def __setattr__(self, name, value):
        self._state.get()[name] = value

    def __getattr__(self, name):
        return self._state.get()[name]

db = peewee.PostgresqlDatabase(
    database=DB_NAME,
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
)
db._state = PeeweeConnectionState()

async def reset_db_state():
    db._state._state.set(db_state_default.copy())
    db._state.reset()

def get_db(db_state=Depends(reset_db_state)):
    try:
        db.connect()
        yield
    finally:
        if not db.is_closed():
            db.close()

def transactional(db_state=Depends(reset_db_state)):
    try:
        db.connect()
        with db.transaction() as txn:
            yield
            txn.commit()
    except Exception as e:
        txn.rollback()
    finally:
        if not db.is_closed():
            db.close()
