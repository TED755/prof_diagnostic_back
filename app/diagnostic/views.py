from django.shortcuts import render
from user.user_model.user_session import *
from .diagnostic_model.diagnostic_activity import *
from .diagnostic_model.diagnostic_helpers import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json

@csrf_exempt
def save_progress(request):
    auth = request.headers['Authorization'].split(' ')
    
    token = UserSession.decode_token(auth[1])
    if 'status' in token:
        return HttpResponse(json.dumps({}), content_type="text/plain", charset='utf-8', status=token['status'])

    try:
        data = json.loads(request.body.decode('utf-8'))
    except ValueError:
        return HttpResponse(
            json.dumps({}), content_type="text/plain", charset='utf-8', status=500)

    # print(token)
    response = DiagnosticActivity.save_progress(user_id=token['user_info']['user_id'], 
        diagnostic_type=data.get('diagnostic_type'), answers=data.get('answers'))

    if 'status' not in response:
        return HttpResponse(json.dumps({'message':'Internal server error'}), 
            content_type="text/plain", charset='utf-8', status=500)

    return HttpResponse(json.dumps({}), content_type="text/plain", charset='utf-8', status=response['status'])

@csrf_exempt
def get_progress(request):
    auth = request.headers['Authorization'].split(' ')
    token = UserSession.decode_token(auth[1])
    if 'status' in token:
        return HttpResponse(json.dumps({}), content_type="text/plain", charset='utf-8', status=token['status'])

    try:
        data = json.loads(request.body.decode('utf-8'))
    except ValueError:
        return HttpResponse(
            json.dumps({}), content_type="text/plain", charset='utf-8', status=500)

    response = {}
    progress = DiagnosticActivity.get_progress(user_id=token['user_info']['user_id'], diagnostic_type=data.get('diagnostic_type'))
    
    if 'data' in progress:
        response['data'] = progress['data']

    return HttpResponse(json.dumps(response), content_type="text/plain", charset='utf-8', status=progress['status'])

@csrf_exempt
def get_diagnostic(request):
    auth = request.headers['Authorization'].split(' ')
    
    token = UserSession.decode_token(auth[1])
    if 'status' in token:
        return HttpResponse(json.dumps({}), content_type="text/plain", charset='utf-8', status=token['status'])

    try:
        data = json.loads(request.body.decode('utf-8'))
    except ValueError:
        return HttpResponse(
            json.dumps({}), content_type="text/plain", charset='utf-8', status=500)

    response = {}

    diagnostic = DiagnosticActivity.get_diagnostic(user_id=token['user_info']['user_id'], 
        diagnostic_type=data.get('diagnostic_type'))

    if 'status' not in diagnostic:
        return HttpResponse(json.dumps({'message':'Internal server error'}), 
            content_type="text/plain", charset='utf-8', status=500)

    if 'data' in diagnostic:
        response['data'] = diagnostic['data']

    return HttpResponse(json.dumps(response), content_type="text/plain", charset='utf-8', status=diagnostic['status'])

@csrf_exempt
def load_recomendations(request):
    auth = request.headers['Authorization'].split(' ')
    
    token = UserSession.decode_token(auth[1])
    if 'status' in token:
        return HttpResponse(json.dumps({}), content_type="text/plain", charset='utf-8', status=token['status'])

    try:
        data = json.loads(request.body.decode('utf-8'))
    except ValueError:
        return HttpResponse(
            json.dumps({}), content_type="text/plain", charset='utf-8', status=500)

    # email = token['user_info']['email']
    # if email != 'develop@admin.com':
    #     return HttpResponse(json.dumps({}), content_type="text/plain", charset='utf-8', status=403)

    result = DiagnosticHelpers.load_recomendations_to_db(data.get('file_name'), data.get('diagnostic_type'))

    return HttpResponse(json.dumps({}), content_type="text/plain", charset='utf-8', status=403)

@csrf_exempt
def get_results(request):
    auth = request.headers['Authorization'].split(' ')
    
    token = UserSession.decode_token(auth[1])
    if 'status' in token:
        return HttpResponse(json.dumps({}), content_type="text/plain", charset='utf-8', status=token['status'])

    if request.method == 'GET':
        result = DiagnosticActivity.get_results(user_id=token['user_info']['user_id'])
    elif request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except ValueError:
            return HttpResponse(
                json.dumps({}), content_type="text/plain", charset='utf-8', status=500)

        result = DiagnosticActivity.get_results(user_id=token['user_info']['user_id'], 
        diagnostic_type=data.get('diagnostic_type'), answers=data.get('answers'))
    else:
        return HttpResponse(json.dumps({}), content_type="text/plain", charset='utf-8', status=400)

    
    response = {}
    if 'data' in result:
        response['data'] = result['data']

    return HttpResponse(json.dumps(response,ensure_ascii=False), 
        content_type="text/plain", charset='utf-8', status=result['status'])

@csrf_exempt
def get_questions(request):
    auth = request.headers['Authorization'].split(' ')
    
    token = UserSession.decode_token(auth[1])
    if 'status' in token:
        return HttpResponse(json.dumps({}), content_type="text/plain", charset='utf-8', status=token['status'])

    diagnostic_type = request.GET['diagnostic_type']
    if not diagnostic_type:
        return HttpResponse(json.dumps({}), status=400)

    questions = DiagnosticActivity.get_questions(diagnostic_type)
    response = {}
    if 'data' in questions:
        response['data'] = questions['data']
    else:
        return HttpResponse(json.dumps({}), content_type="text/plain", charset='utf-8', status=500)
        
    return HttpResponse(json.dumps(response,ensure_ascii=False), content_type="text/plain", charset='utf-8', status=questions['status'])