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
    # print(token)
    if 'status' in token:
        return HttpResponse(json.dumps({'message': token['message']}),
                            content_type="application/json", charset='utf-8', status=token['status'])

    if not UserSession.validate_refresh_token(token):
        return HttpResponse(json.dumps({'message': 'Not valid token'}),
                            content_type="application/json", charset='utf-8', status=401)
    # print(session_expired)

    # if not UserSession.end_session_if_not_active(token=token):
    #     return HttpResponse(json.dumps({}), content_type="application/json", charset='utf-8', status=500)
    # session_expired = UserSession.session_expired(token=token)
    # if 'data' in session_expired:
    #     if session_expired['data']:
    #         if not UserSession.end_session(session_expired['data']['session_id']):
    #             return HttpResponse(json.dumps({}), content_type="application/json", charset='utf-8', status=500)
    #         return HttpResponse(json.dumps({}), content_type="application/json", charset='utf-8', status=session_expired['status'])
    # else:
    #     return HttpResponse(json.dumps({}), content_type="application/json", charset='utf-8', status=session_expired['status'])

    refresh = UserActivity.refresh_tokens(token)

    if refresh['status'] != 201:
        return HttpResponse(json.dumps({}, content_type="application/json", charset='utf-8', status=refresh['status']))

    response = {}

    if 'data' in  refresh:
        response['data'] = refresh['data']
    
    return HttpResponse(json.dumps(response), content_type="application/json", charset='utf-8', status=refresh['status'])

@csrf_exempt
def end_session(request):
    if request.method != 'GET':
        return HttpResponse(json.dumps({}), content_type="application/json", charset='utf-8', status=400)

    auth = request.headers['Authorization'].split(' ')
    
    token = UserSession.decode_token(auth[1])

    if 'status' in token:
        return HttpResponse(json.dumps({}), content_type="application/json", charset='utf-8', status=token['status'])

    if UserSession.end_session_if_not_active(token=token):
        return HttpResponse(json.dumps({}), content_type="application/json", charset='utf-8', status=400)
    
    if not UserSession.end_session(user_id=token['user_info']['user_id']):
        return HttpResponse(json.dumps({}), content_type="application/json", charset='utf-8', status=500)
    
    return HttpResponse(json.dumps({}), content_type="application/json", charset='utf-8', status=200)

    
@csrf_exempt
def get_teaching_exp(request):
    if request.method != 'GET':
        return HttpResponse(json.dumps({}), content_type="application/json", charset='utf-8', status=400)

    response = response = {
        "data": UserHelpers.get_register_data('teaching_exp')
    }

    return HttpResponse(json.dumps(response), content_type="application/json", charset='utf-8', status=200)

@csrf_exempt
def get_position(request):
    if request.method != 'GET':
        return HttpResponse(json.dumps({}), content_type="application/json", charset='utf-8', status=400)

    response = {
        "data": UserHelpers.get_register_data('position')
    }

    return HttpResponse(json.dumps(response), content_type="application/json", charset='utf-8', status=200)

@csrf_exempt
def get_category(request):
    if request.method != 'GET':
        return HttpResponse(json.dumps({}), content_type="application/json", charset='utf-8', status=400)

    response = {
        "data": UserHelpers.get_register_data('category')
    }

    return HttpResponse(json.dumps(response), content_type="application/json", charset='utf-8', status=200)

@csrf_exempt
def get_raion(request):
    if request.method != 'GET':
        return HttpResponse(json.dumps({}), content_type="application/json", charset='utf-8', status=400)

    response = {
        "data": UserHelpers.get_register_data('raion')
    }

    return HttpResponse(json.dumps(response), content_type="application/json", charset='utf-8', status=200)

@csrf_exempt
def get_region_rf(request):
    if request.method != 'GET':
        return HttpResponse(json.dumps({}), content_type="application/json", charset='utf-8', status=400)

    response = {
        "data": UserHelpers.get_register_data('region_rf')
    }

    return HttpResponse(json.dumps(response), content_type="application/json", charset='utf-8', status=200)

@csrf_exempt
def get_locality_type(request):
    if request.method != 'GET':
        return HttpResponse(json.dumps({}), content_type="application/json", charset='utf-8', status=400)

    response = {
        "data": UserHelpers.get_register_data('locality_type')
    }

    return HttpResponse(json.dumps(response), content_type="application/json", charset='utf-8', status=200)
