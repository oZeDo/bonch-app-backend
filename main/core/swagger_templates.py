from drf_yasg import openapi
from rest_framework import status


LoginRequest = {
    "method": "post",
    "operation_description": "Получить токен авторизации:",
    "request_body": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["username", "password"],
        properties={
            'username': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Логин',
                example="admin@gmail.com"
            ),
            'password': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Пароль',
                example="qwerty123"
            )
        },
    ),
    "responses": {status.HTTP_200_OK: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
                'Token': openapi.Schema(type=openapi.TYPE_STRING, example="9da4a5d906377bf433a5ff543b87632ea0e9214b"),
            }
        )
    }
}

