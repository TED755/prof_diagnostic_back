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
                'user_id': user.id,
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

    def create_user(data):
        if (not data.get('name') or 
            not data.get('email') or 
            not data.get('password')):
                return {'status':400, 'message':'Name, email or password were not given'}
        user = User(
            name = data.get('name'),
            email = data.get('email'),
            password = UserHelpers.crypt_password(data.get('password')),
            category = data.get('category') if data.get('category') else '',
            teaching_exp = data.get('teaching_exp') if data.get('teaching_exp') else '',
            position = data.get('position') if data.get('position') else '',
            raion = data.get('raion') if data.get('raion') else '',
            region_rf = data.get('region_rf') if data.get('region_rf') else '',
            school = data.get('school') if data.get('school') else '',
            locality_type = data.get('locality_type') if data.get('locality_type') else ''
        )

        user.save()
        return {'status':201, 'message':'success', 'data':UserHelpers.user_info(user)}