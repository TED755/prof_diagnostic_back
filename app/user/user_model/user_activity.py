from user.models import *
from .user_helpers import UserHelpers
from .user_session import UserSession
import json

class UserActivity():
    def login(data: json) -> User:
        _users = UserHelpers.find_user_by_email(data.get('email'))
        if not _users:
            return None

        _user = _users[0]
        if not UserHelpers.check_password(_user, data.get('password')):
            return None
        
        session = UserSession.create_session(user=_user)
        # print (f"{session.user_id}, {session.start_date}, {session.start_time}")
        # key = 'secret' # Разные для каждого пары?
        
        # return json {'user_id', tokens{refresh, access}, user_info}
        return _user

    # def crypt_password(password):
    #     return password
    # def decrypt_password(password):
    #     return password

    # def find_user_by_email(email):
    #     return User.objects.filter(email=email)
    
    # def check_password(user: User, password):
    #     return UserActivity.decrypt_password(user.password) == password
    
    