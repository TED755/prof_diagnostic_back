from user.models import User
from .user_helpers import UserHelpers
from datetime import datetime, timedelta
import json
import jwt
JWT_ACCESS_TTL = 300 # seconds
JWT_REFRESH_TTL = 3600 * 24 * 7
class UserActivity():
    def login(data: json) -> User:
        _users = UserHelpers.find_user_by_email(data.get('email'))
        if not _users:
            return None

        _user = _users[0]
        if not UserHelpers.check_password(_user, data.get('password')):
            return None
        
        key = 'secret' # Разные для каждого пары?
        access_token = jwt.encode({
            'iss': 'backend-api',
            'exp': datetime.utcnow() + timedelta(seconds=JWT_ACCESS_TTL),
            'user_id': _user.id,
            'user_info': UserHelpers.json_user(_user),
            'type': 'access'
        }, key)
        # print(access_token)
        # decoded = jwt.decode(access_token, key)
        # print(decoded)

        refresh_token = jwt.encode({
            'iss': 'backend-api',
            'exp': datetime.utcnow() + timedelta(seconds=JWT_REFRESH_TTL),
            'user_id': _user.id,
            'user_info': UserHelpers.json_user(_user),
            'type': 'refresh'
        }, key)
        print(json.dumps({'tokens':{
            'access': access_token,
            'refresh': refresh_token
        }}))
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
    
    