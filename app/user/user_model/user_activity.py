from user.models import *
from .user_helpers import UserHelpers
from .user_session import UserSession
from prof_diagnostic.settings import JWT_ACCESS_TTL, JWT_REFRESH_TTL
import json

# JWT_ACCESS_TTL = 300 # seconds
# JWT_REFRESH_TTL = 3600 * 24 * 7

class UserActivity():
    def login(data: json) -> hash:
        _users = UserHelpers.find_user_by_email(data.get('email'))
        if not _users:
            # return json.dumps({'message':'Invalid email or password'})
            return {'status':401, 'message':'Invalid email or password'}

        _user = _users[0]
        if not UserHelpers.check_password(_user, data.get('password')):
            # return json.dumps({'message':'Invalid email or password'})
            return {'status':401, 'message':'Invalid email or password'}
        
        session = UserSession.create_session(user=_user)
        tokens = UserHelpers.create_tokens(user=_user)

        # response = json.dumps({
        #     'message': 'success',
        #     'data': {
        #         'access': session.access_token,
        #         'refresh': session.refresh_token,
        #         'refresh_access_in': JWT_ACCESS_TTL,
        #         'refresh_in': JWT_REFRESH_TTL
        #     }
        # }, ensure_ascii=False)

        if session['status'] == 201:
            response = {
                'status': 201,
                'message': session['message'],
                'data': {
                    'access': tokens['access'],
                    'refresh': tokens['refresh'],
                    'refresh_access_in': JWT_ACCESS_TTL,
                    'refresh_in': JWT_REFRESH_TTL
                }
            }
        if session['status'] == 208:
            response = {
                'status': 208,
                'message': session['message'],
            }

        # print(jwt.decode(session.access_token, 'secret', algorithms="HS256"))
        

        # print (f"{session.user_id}, {session.start_date}, {session.start_time}")
        # key = 'secret' # Разные для каждого пары?
        
        # return json {'user_id', tokens{refresh, access}, user_info}
        return response

    # def crypt_password(password):
    #     return password
    # def decrypt_password(password):
    #     return password

    # def find_user_by_email(email):
    #     return User.objects.filter(email=email)
    
    # def check_password(user: User, password):
    #     return UserActivity.decrypt_password(user.password) == password
    
    