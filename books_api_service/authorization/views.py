from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny

from django.contrib.auth.models import User


from .serializers import UserSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Создание нового пользователя для проверки работы способности авторизации и разлогирования",
        tags=["Auth"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD),

            },
            required=['username', 'password']
        ),
        operation_description="Используется стандартный юзер джанго. для простоты не стал ничего писать и взял готовое. при необходимости кастомизировать можно пользователя"
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)




from django.contrib.auth import logout
from django.http import JsonResponse
from django.views import View

class LogoutView(View):
    '''
    переопредленная стандартное рестовское представление для лог аута
    создан путь и повешен на Ui-rest framework и swagger-ui (django logout)
    '''

    def get(self, request, *args, **kwargs):
        logout(request)
        return JsonResponse({'message': 'Successfully logged out get.'})

    # def post(self, request, *args, **kwargs):
    #     logout(request)
    #     return JsonResponse({'message': 'Successfully logged out post запрос.'})