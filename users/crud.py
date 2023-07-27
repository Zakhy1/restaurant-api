from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from models import User


class UserOperations:
    def __init__(self, engine):
        self.engine = engine

    def get_user(self, username, password):
        with Session(self.engine) as session:
            query = select(User).where(and_(User.username == username, User.password == password))
            user = session.execute(query).scalar_one_or_none()
            if user:
                return {"id": str(user.id), "username": user.username}
            else:
                return None
