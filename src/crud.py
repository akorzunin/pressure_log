from tinydb import where
from tinydb.table import Table
from src import shemas


def get_user(db, user_id: int) -> dict:
    return db.get(where("user_id") == user_id)


def create_user(
    db: Table,
    user: shemas.User,
) -> shemas.User:
    if not db.get(where("user_id") == user.user_id):
        db.insert(user.dict())
        return user


def update_user(
    db: Table,
    user: shemas.User,
    user_id: str,
) -> shemas.User:
    if user_upd := {k: v for k, v in user.dict().items() if v is not None}:
        db.update(user_upd, where("user_id") == user_id)
        return db.get(where("user_id") == user_id)


def delete_user(db: Table, user_id: str):
    if db.get(where("user_id") == user_id):
        return db.remove(where("user_id") == user_id)
