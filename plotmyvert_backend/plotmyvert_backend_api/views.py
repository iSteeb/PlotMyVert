from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import User
from django.http import JsonResponse
import json
from .lib import *
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .serializers import *

@ensure_csrf_cookie
def setCsrfCookie(request):
    return JsonResponse({"success": True})

def getAllSessions(request):
    if request.method == 'POST':
        user = User.objects.get(pk=request.user.get_username())
        sessions = JumpSessionModel.objects.filter(user=user)
        serializer = JumpSessionModelSerializer(sessions, many=True)
        return JsonResponse({"success": True, "sessions": serializer.data})
    else:
        return JsonResponse({"message": "Invalid request method."}, status=405)

def getJumpsFromSession(request):
    if request.method == 'POST':
        user = User.objects.get(pk=request.user.get_username())
        start_datetime = json.loads(request.body.decode('utf-8')).get('start_datetime')

        session = JumpSessionModel.objects.filter(start_datetime=start_datetime).filter(user=user).first()
        serializer = JumpSessionModelSerializer(session, many=False)
        jumps = JumpSessionJumpsModel.objects.filter(session=session)
        serializer = JumpSessionJumpsModelSerializer(jumps, many=True)
        return JsonResponse({"success": True, "jumps": serializer.data})
    else:
        return JsonResponse({"message": "Invalid request method."}, status=405)

def getNewSessionsFromEmail(request):
    if request.method == 'POST':
        user = User.objects.get(pk=request.user.get_username())
        config = user.get_config()
        try:
            M = login_to_email(config['mail_SSL'], config['mail_server'], config['mail_port'], config['receive_email_login'], config['receive_email_password'])
            mail_ids = select_session_emails(M, config['receive_email_receiver'])
            files = get_all_new_data_from_emails(M, mail_ids)
            mark_emails_for_delete(M, mail_ids)
            logout_from_email(M)

            new_sessions = []

            for f in files:
                dataframe = generate_dataframe_from_excel(f, user)
                if dataframe is None:
                    continue
                plot = generate_plot_from_dataframe(dataframe)
                jump_session_database_entry = save_jump_session_to_database(user, dataframe, plot)
                save_jump_session_jumps_to_database(jump_session_database_entry, dataframe)

                new_sessions.append(jump_session_database_entry)
            
            serializer = JumpSessionModelSerializer(new_sessions, many=True)

            return JsonResponse({"success": True, "sessions": serializer.data})
        except Exception as e:
            print(e)
            return JsonResponse({"message": "Something went wrong."}, status=401)
    else:
        return JsonResponse({"message": "Invalid request method."}, status=405)

def signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email')
            password = data.get('password')
            User.objects.create_user(email=email, password=password)
            return JsonResponse({"success": True})
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON data."}, status=400)
    else:
        return JsonResponse({"message": "Invalid request method."}, status=405)

def userLogin(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email')
            password = data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"message": "Invalid username or password."}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON data."}, status=400)
    else:
        return JsonResponse({"message": "Invalid request method."}, status=405)

def checkLoginStatus(request):
    if request.user.is_authenticated:
        return JsonResponse({"isLoggedIn": True})
    else:
        return JsonResponse({"isLoggedIn": False})

def userLogout(request):
    if request.method == 'GET':
        logout(request)
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"message": "Invalid request method."}, status=405)

def getUserConfig(request):
    if request.method == 'POST':
        try:
            email = request.user.get_username()
            return JsonResponse(User.objects.get(pk=email).get_config())
        except json.JSONDecodeError:
            return JsonResponse({"message": "crap"}, status=400)
    else:
        return JsonResponse({"message": "Invalid request method."}, status=405)

def configure(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email')
            password = data.get('password')
            recipient = data.get('recipient')
            host = data.get('host')
            port = data.get('port')
            ssl = data.get('ssl')
            user = User.objects.get(pk=request.user.get_username())
            
            if user is not None:
                user.receive_email_login = email
                user.receive_email_password = password
                user.receive_email_receiver = recipient
                user.mail_server = host
                user.mail_port = port
                user.mail_SSL = ssl
                user.save()
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"message": "Something went wrong."}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON data."}, status=400)
    else:
        return JsonResponse({"message": "Invalid request method."}, status=405)