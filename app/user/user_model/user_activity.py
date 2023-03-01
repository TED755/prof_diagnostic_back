from user.models import *
from .user_helpers import UserHelpers
from .user_session import UserSession
import json

JWT_ACCESS_TTL = 300 # seconds
JWT_REFRESH_TTL = 3600 * 24 * 7

class UserActivity():
     # response: json {'status','erorr','user_id', tokens{refresh, access}, user_info}
    def login(data: json) -> json:
        _users = UserHelpers.find_user_by_email(data.get('email'))
        if not _users:
            # return json.dumps({'message':'Invalid email or password'})
            return {'message':'Invalid email or password'}

        _user = _users[0]
        if not UserHelpers.check_password(_user, data.get('password')):
            # return json.dumps({'message':'Invalid email or password'})
            return {'message':'Invalid email or password'}
        
        session = UserSession.create_session(user=_user)

        # response = json.dumps({
        #     'message': 'success',
        #     'data': {
        #         'access': session.access_token,
        #         'refresh': session.refresh_token,
        #         'refresh_access_in': JWT_ACCESS_TTL,
        #         'refresh_in': JWT_REFRESH_TTL
        #     }
        # }, ensure_ascii=False)

        response = {
            'message': 'success',
            'data': {
                'access': session.access_token,
                'refresh': session.refresh_token,
                'refresh_access_in': JWT_ACCESS_TTL,
                'refresh_in': JWT_REFRESH_TTL
            }
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
    
    