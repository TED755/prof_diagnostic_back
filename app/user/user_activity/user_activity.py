from user.models import User
from .user_helpers import UserHelpers
import json

class UserActivity():
    def login(data: json) -> User:
        _users = UserHelpers.find_user_by_email(data.get('email'))
        if not _users:
            return None

        _user = _users[0]
        if not UserHelpers.check_password(_user, data.get('password')):
            return None
        return _user

    # def crypt_password(password):
    #     return password
    # def decrypt_password(password):
    #     return password

    # def find_user_by_email(email):
    #     return User.objects.filter(email=email)
    
    # def check_password(user: User, password):
    #     return UserActivity.decrypt_password(user.password) == password
    
    