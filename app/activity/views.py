# from django.shortcuts import render
# from django.http import HttpResponse
# from werkzeug.security import generate_password_hash, check_password_hash
# # from .models import Activity
# from django.views.decorators.csrf import csrf_exempt
# import json

# @csrf_exempt
# def register(request):
#     try:
#         data = json.loads(request.body.decode())
#     except ValueError:
#         return HttpResponse({
#             'error': 'bla bla bla',
#         })

#     print(data.get('email'))
#     # activity = Activity(request)
#     # activity.register_user()
#     # activity.register_user()
#     # print (activity)
#     return HttpResponse(request, {'email': data.get('email'), 'password': data.get('password')})

# @csrf_exempt
# def login(request):
#     right_email = 'test_user1@test.com'
#     right_password = '123'
#     try:
#         data = json.loads(request.body.decode())
#     except ValueError:
#         return HttpResponse({
#             'error': 'bla bla bla',
#         })

#     email = data.get('email')
#     password = data.get('password')

#     if email == right_email and password == right_password:
#         return HttpResponse(request, json.dumps({'name':'Test User One', 'email':email, 'status':'OK'}))
#     else: return HttpResponse(request, json.dumps({'email':email, 'error':'Invalid email or password'}))
