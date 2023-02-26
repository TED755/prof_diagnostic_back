from user.models import User
from datetime import datetime, timedelta
import jwt
import json

JWT_ACCESS_TTL = 300 # seconds
JWT_REFRESH_TTL = 3600 * 24 * 7
JWT_SECRET_KEY = 'secret'

class UserHelpers():
    def crypt_password(password):
        return password
    def decrypt_password(password):
        return password

    def find_user_by_email(email):
        return User.objects.filter(email=email)
    
    def check_password(user: User, password):
        return UserHelpers.decrypt_password(user.password) == password

    def json_user(user: User):
        return {'email': user.email}

    def create_tokens(user: User):
        access_token = jwt.encode({
            'iss': 'backend-api',
            'exp': datetime.utcnow() + timedelta(seconds=JWT_ACCESS_TTL),
            'user_id': user.id,
            'user_info': UserHelpers.json_user(user),
            'type': 'access'
        }, JWT_SECRET_KEY)
        # print(access_token)
        # decoded = jwt.decode(access_token, key)
        # print(decoded)

        refresh_token = jwt.encode({
            'iss': 'backend-api',
            'exp': datetime.utcnow() + timedelta(seconds=JWT_REFRESH_TTL),
            'user_id': user.id,
            'user_info': UserHelpers.json_user(user),
            'type': 'refresh'
        }, JWT_SECRET_KEY)
    
        return {
            'access': access_token,
            'refresh': refresh_token
        }