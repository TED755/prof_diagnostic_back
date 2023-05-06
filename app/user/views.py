# from django.shortcuts import render
from django.http import HttpResponse
# from .models import User
from django.views.decorators.csrf import csrf_exempt
import json
from user.user_model.user_activity import *

@csrf_exempt
def register(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except ValueError:
        return HttpResponse(
            json.dumps({}), content_type="application/json", charset='utf-8', status=500)

    _response = UserActivity.register(data)
    response = {}
    if 'data' in _response:
        response['data'] = _response['data']

    return HttpResponse(json.dumps(response), content_type="application/json", charset='utf-8', status=_response['status'])

@csrf_exempt
def login(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except ValueError:
        return HttpResponse(
            json.dumps({}), content_type="application/json", charset='utf-8', status=500)

    login_user = UserActivity.login(data)

    response = {}
    if 'data' in login_user:
        response['data'] = login_user['data']

    return HttpResponse(json.dumps(response), content_type="application/json", charset='utf-8', status=login_user['status'])

@csrf_exempt
def refresh(request):
    # auth = request.headers['Authorization'].split(' ')
    # token = UserSession.decode_token(auth[1])
    try:
        data = json.loads(request.body.decode('utf-8'))
    except ValueError:
        return HttpResponse(
            json.dumps({}), content_type="application/json", charset='utf-8', status=500)
    
    token = UserSession.decode_token(data.get('refresh'))
    if 'status' in token:
        return HttpResponse(json.dumps({}), content_type="application/json", charset='utf-8', status=token['status'])

    # TODO: check session token expired
    # check session not expired
    session_expired = UserSession.session_expired(refresh_token=token)
    if 'data' in session_expired:
        print(session_expired['data'])
        if session_expired['data']:
            return HttpResponse(json.dumps({}), content_type="application/json", charset='utf-8', status=token['status'])
    else:
        return HttpResponse(json.dumps({}), content_type="application/json", charset='utf-8', status=token['status'])

    refresh = UserActivity.refresh_tokens(token)

    if refresh['status'] != 201:
        return HttpResponse(json.dumps({}), content_type="application/json", charset='utf-8', status=refresh['status'])

    response = {}

    if 'data' in  refresh:
        response['data'] = refresh['data']
    
    return HttpResponse(json.dumps(response), content_type="application/json", charset='utf-8', status=refresh['status'])

@csrf_exempt
def end_session(request):
    pass

# @csrf_exempt
# def profile(request):
#     try:
#         data = json.loads(request.body.decode('utf-8'))
#     except ValueError:
#         return HttpResponse(
#             json.dumps({}), content_type="application/json", charset='utf-8', status=500)
        
#     token = UserSession.decode_token(data.get('access'))

#     if 'status' in token:
#         return HttpResponse(json.dumps({}), content_type="application/json", charset='utf-8', status=token['status'])

    