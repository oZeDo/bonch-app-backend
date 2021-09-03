from drf_yasg import openapi
from rest_framework import status


EventsRequest = {
    "method": "get",
    "operation_description": "Получить все мероприятия",
    "responses": {
        status.HTTP_200_OK: openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'name': openapi.Schema(type=openapi.TYPE_STRING, example="Умка"),
                    'picture': openapi.Schema(type=openapi.TYPE_STRING, example="https://lk.sut.ru/cabinet/ini/subconto"
                                                                                "/sendto/101/1578741/0fppitn9whs.jpg"),
                    'description': openapi.Schema(type=openapi.TYPE_STRING, example="Зимняя сессия не за горами, уверен"
                                                                                    "ы, что Вы устали готовиться к ней,"
                                                                                    " так же как и мы. Но как Вы смотри"
                                                                                    "те на то, чтобы напрячь свои мозги"
                                                                                    " и повеселиться вместе с нами?"),
                    'uuid': openapi.Schema(type=openapi.TYPE_STRING, example="ab7e77bc-4097-11eb-b378-0242ac130002"),
                    'timestamp': openapi.Schema(type=openapi.TYPE_STRING, example="2020-11-25 18:00:00.000000 +00:00"),
                },
            )
        ),
    }
}

# tmp = {
#     "key": field.key,
#     "name": field.name,
#     "type": field.type,
#     "required": field.required,
#     "extra": []
# }
EventFormRequest = {
    "method": "get",
    "operation_description": "Получить форму регистрации мероприятия",
    "manual_parameters": [
        openapi.Parameter(
            name="uuid",
            type=openapi.TYPE_STRING,
            description="Универсальный уникальный идентификатор мероприятия",
            in_=openapi.IN_PATH
        ),
    ],
    "responses": {
        status.HTTP_200_OK: openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "key": openapi.Schema(type=openapi.TYPE_STRING, example="ab7e77bc-4097-11eb-b378-0242ac130002"),
                    "name": openapi.Schema(type=openapi.TYPE_STRING, example="Время проведения викторины"),
                    "type": openapi.Schema(type=openapi.TYPE_STRING, example="M"),
                    "required":  openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                    "extra":  openapi.Schema(
                        type=openapi.TYPE_OBJECT, properties={
                            "1": openapi.Schema(type=openapi.TYPE_STRING, example="11:00"),
                            "2": openapi.Schema(type=openapi.TYPE_STRING, example="12:00"),
                            "3": openapi.Schema(type=openapi.TYPE_STRING, example="13:00"),
                            "4": openapi.Schema(type=openapi.TYPE_STRING, example="14:00"),
                            "5": openapi.Schema(type=openapi.TYPE_STRING, example="15:00"),
                            "other": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                        }
                    )
                },
            )
        )
    },
}