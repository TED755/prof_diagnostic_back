from django.db import models
from users.user import user

# I don't understand how it's works but i need suka
class Activity(models.Model):
    def __init__(self, request):
        self.users = []
        # self.users.append(user.User('evgen', 'dd@aa.com', 'sdfs'))
        # sessions = []
    
    def register_user(self):
        if not self.check_user_reg(user.User('evgen', 'dd@aa.com', 'sdfs')):
            self.users.append(user.User('evgen', 'dd@aa.com', 'sdfs'))
        print(self.users)

    def check_user_reg(self, _user: user.User):
        f_user = self.get_user_by_email(email=_user.email)
        return f_user != None

    def get_user_by_email(self, email: str) -> user.User:
        for user in self.users:
            if user.email == email:
                return user

    # def login():
    #     pass
        
    # user = user.User('evgen', 'dd@aa.com', 'sdfs')
    # print('a')
    