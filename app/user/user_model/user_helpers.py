import json
import os
from user.models import User

class UserHelpers():
    def crypt_password(password):
        return password
    def decrypt_password(password):
        return password

    def find_user_by_email(email):
        return User.objects.filter(email=email)
    
    def check_password(user: User, password):
        return UserHelpers.decrypt_password(user.password) == password

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
        return {'status':201, 'message':'success', 'data':user.user_info()}
    
    def get_register_data(parameter: str)->list:
        data_path = 'files/registration_data.json'

        if not os.path.exists(data_path):
            return {'status':500, 'message':'Internal server error'}

        with open(data_path, 'r', encoding='utf-8') as f: #открыли файл с данными
            register_data = json.load(f)

        f.close()

        return register_data[parameter]