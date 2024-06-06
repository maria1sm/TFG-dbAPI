from sqlalchemy.orm import Session
from persistence.model.users import User
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

class UserService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_user_by_id(self, user_id: str):
        return self.db_session.query(User).filter(User.id == user_id).first()

    def get_users_by_country(self, country: str):
        return self.db_session.query(User).filter(User.country == country).all()

    def get_all_users(self):
        return self.db_session.query(User).all()

    def insert_user(self, user_data: dict):
        user_exists = check_user_exists(self, user_data['id'])
        if user_exists:
            return False

        user_data['register_date'] = datetime.now()
        user = User(**user_data)
        self.db_session.add(user)
        self.db_session.commit()
        return True

def check_user_exists(self, user_id: str) -> bool:
        # Query the database for a user with the specified ID
        user = self.db_session.query(User).filter(User.id == user_id).first()
        # If user is not None, it means the user exists
        return user is not None