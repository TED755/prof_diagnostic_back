from user.models import User
from datetime import datetime, timedelta
import jwt
from prof_diagnostic.settings import SECRET_KEY, JWT_REFRESH_TTL, JWT_ACCESS_TTL

class UserHelpers():
    def crypt_password(password):
        return password
    def decrypt_password(password):
        return password

    def find_user_by_email(email):
        return User.objects.filter(email=email)
    
    def check_password(user: User, password):
        return UserHelpers.decrypt_password(user.password) == password

    def user_info(user: User):
        return {
                'email': user.email,
                'name': user.name,
                'category': user.category,
                'teaching_exp': user.teaching_exp,
                'position': user.position,
                'raion': user.raion,
                'region_rf': user.region_rf,
                'school': user.school,
                'locality_type': user.locality_type
            }

    def create_tokens(user: User):
        access_token = jwt.encode({
            'iss': 'backend-api',
            'exp': datetime.utcnow() + timedelta(seconds=JWT_ACCESS_TTL),
            'iat': datetime.utcnow(),
            'user_id': user.id,
            'user_info': UserHelpers.user_info(user),
            'type': 'access'
        }, SECRET_KEY, algorithm='HS256')
        # print(access_token)
        # print(jwt.decode(access_token, SECRET_KEY, algorithms='HS256'))
        # print(access_token)
        # decoded = jwt.decode(access_token, key)
        # print(decoded)

        refresh_token = jwt.encode({
            'iss': 'backend-api',
            'exp': datetime.utcnow() + timedelta(seconds=JWT_REFRESH_TTL),#JWT_REFRESH_TTL,#
            'iat': datetime.utcnow(),
            'user_id': user.id,
            'user_info': UserHelpers.user_info(user),
            'type': 'refresh'
        }, SECRET_KEY, algorithm='HS256')

        # print(refresh_token)
        # print(jwt.decode(refresh_token, SECRET_KEY, algorithms='HS256'))
    
        return {
            'access': access_token,
            'refresh': refresh_token
        }