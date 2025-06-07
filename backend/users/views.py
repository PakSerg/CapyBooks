from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json


@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            if not all([username, password]):
                return JsonResponse({
                    'error': 'Все поля обязательны для заполнения'
                }, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({
                    'error': 'Пользователь с таким именем уже существует'
                }, status=400)

            user = User.objects.create_user(
                username=username,
                password=password
            )

            return JsonResponse({
                'message': 'Пользователь успешно зарегистрирован',
                'user': {
                    'id': user.id,
                    'username': user.username,
                }
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({
                'error': 'Неверный формат данных'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'error': str(e)
            }, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            if not all([username, password]):
                return JsonResponse({
                    'error': 'Все поля обязательны для заполнения'
                }, status=400)

            user = authenticate(username=username, password=password)

            if user is None:
                return JsonResponse({
                    'error': 'Неверные учетные данные'
                }, status=401)

            login(request, user)

            return JsonResponse({
                'message': 'Успешный вход',
                'user': {
                    'id': user.id,
                    'username': user.username,
                }
            })

        except json.JSONDecodeError:
            return JsonResponse({
                'error': 'Неверный формат данных'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'error': str(e)
            }, status=500)
