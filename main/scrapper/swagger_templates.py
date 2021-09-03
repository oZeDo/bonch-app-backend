from drf_yasg import openapi
from rest_framework import status

AccountRequest = {
    "method": "get",
    "operation_description": "Получить информацию о пользователе",
    "responses": {status.HTTP_200_OK: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "fullname": openapi.Schema(type=openapi.TYPE_STRING, example="Балуев Михаил Евгеньевич"),
            "group": openapi.Schema(type=openapi.TYPE_STRING, example="ИКТ-616"),
            "faculty": openapi.Schema(type=openapi.TYPE_STRING, example="Инфокоммуникационных сетей и систем "
                                                                        "(ИКСС)"),
            "course": openapi.Schema(type=openapi.TYPE_INTEGER, example=2),
            "birth_date": openapi.Schema(type=openapi.TYPE_STRING, example="2000-11-24T00:00:00Z"),
        },
    )
    },
}

MarkRequest = {
    "method": "get",
    "operation_description": "Получить зачетку пользователя",
    "responses": {
        status.HTTP_200_OK: openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "course": openapi.Schema(type=openapi.TYPE_INTEGER, example=2),
                    "semester": openapi.Schema(type=openapi.TYPE_INTEGER, example=3),
                    "subject": openapi.Schema(type=openapi.TYPE_STRING, example="Физические основы электроник"),
                    "mark": openapi.Schema(type=openapi.TYPE_STRING, example="Зачтено"),
                },
            )
        )
    },
}
DebtRequest = {
    "method": "get",
    "operation_description": "Получить задолженности пользователя",
    "responses": {
        status.HTTP_200_OK: openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "course": openapi.Schema(type=openapi.TYPE_INTEGER, example=2),
                    "semester": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                    "subject": openapi.Schema(type=openapi.TYPE_STRING, example="Математика"),
                    "subject_type": openapi.Schema(type=openapi.TYPE_STRING, example="Экзамен"),
                },
            )
        )
    },
}
HistoryRequest = {
    "method": "get",
    "operation_description": "Получить историю факультативов пользователя",
    "responses": {
        status.HTTP_200_OK: openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "subject": openapi.Schema(type=openapi.TYPE_STRING,
                                              example="Программирование микроконтроллеров STM32"),
                    "status": openapi.Schema(type=openapi.TYPE_STRING, example="Принят"),
                    "mark": openapi.Schema(type=openapi.TYPE_STRING, example="ведомости нет"),
                },
            )
        )
    },
}
ContactRequest = {
    "method": "get",
    "operation_description": "Получить список преподавателей, которым можно написать",
    "responses": {
        status.HTTP_200_OK: openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "name": openapi.Schema(type=openapi.TYPE_STRING, example="Борисов Сергей Петрович"),
                    "send_to": openapi.Schema(type=openapi.TYPE_INTEGER, example=12345),
                },
            )
        )
    },
}
ConversationsRequest = {
    "method": "get",
    "operation_description": "Получить все сообщения",
    "responses":  {
        status.HTTP_200_OK: openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=164430),
                    "date": openapi.Schema(type=openapi.TYPE_STRING, example="2020-03-27T15:57:13Z"),
                    "text": openapi.Schema(type=openapi.TYPE_STRING, example="Уважаемые студенты!"),
                    "read": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                    "addressed_id": openapi.Schema(type=openapi.TYPE_INTEGER, example=164430),
                    "type": openapi.Schema(type=openapi.TYPE_STRING, example="in"),
                    "subject": openapi.Schema(type=openapi.TYPE_STRING, example="Зачет"),
                    "destination": openapi.Schema(type=openapi.TYPE_STRING, example="Балуев Андрей Константинович"),
                    "files": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "name": openapi.Schema(type=openapi.TYPE_STRING, example="image.png"),
                            "url": openapi.Schema(type=openapi.TYPE_STRING,
                                                  example="https://lk.sut.ru/cabinet/ini/subconto/sendto/10/"
                                                          "616830/image.png")
                            }
                        )
                    ),
                }
            )
        )
    }
}
MessageDeleteRequest = {
    "method": "delete",
    "operation_description": "Удалить сообщения",
    "request_body": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "message": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                description="Массив с id сообщений",
                items=openapi.Schema(type=openapi.TYPE_INTEGER, example=611233)
            ),
        },
    ),
    "responses": {
        status.HTTP_200_OK: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "detail": openapi.Schema(type=openapi.TYPE_STRING, example="Успех."),
            }
        ),
        status.HTTP_404_NOT_FOUND: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "detail": openapi.Schema(type=openapi.TYPE_STRING, example="Сообщение с id 607122 не найдено."),
            }
        )
    }
}
MessageSendRequest = {
    "method": "post",
    "operation_description": "Отправить/ответить на сообщение\nОбщий размер файлов не должен превышать 5мб, количество "
                             "файлов не ограничено. В сообщении должен присутствовать text или file",
    "request_body": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["message_type"],
        properties={
            "text": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Текст сообщения"
            ),
            "subject": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Тема сообщения, указывается только для message_type=new",
            ),
            "message_type": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Тип сообщения\nОтвет на другое сообщение/отправка нового",
                enum=["reply", "new"],
            ),
            "item": openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description="id сообщения на которое хотим ответить/id пользователя которому хотим написать",
            ),
            "files": openapi.Schema(
                description="Файлы сообщения",
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "name": openapi.Schema(type=openapi.TYPE_STRING),
                        "byte_string": openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
        },
    ),
}
# MessageSendRequest = {
#     "method": "post",
#     "operation_description": "Отправить/ответить на сообщение\nОбщий размер файлов не должен превышать 5мб, количество "
#                              "файлов не органичено. В сообщении должен присутствовать text или file",
#     "manual_parameters": [
#         openapi.Parameter(
#             name="text",
#             type=openapi.TYPE_STRING,
#             description="Текст сообщения",
#             in_=openapi.IN_FORM
#         ),
#         openapi.Parameter(
#             name="subject",
#             type=openapi.TYPE_STRING,
#             description="Тема сообщения, указывается только для message_type=new",
#             in_=openapi.IN_FORM
#         ),
#         openapi.Parameter(
#             name="message_type",
#             type=openapi.TYPE_STRING,
#             required=True,
#             enum=["reply", "new"],
#             description="Тип сообщения\nОтвет на другое сообщение/отправка нового",
#             in_=openapi.IN_FORM
#         ),
#         openapi.Parameter(
#             name="item",
#             type=openapi.TYPE_INTEGER,
#             description="id сообщения на которое хотим ответить/id пользователя которому хотим написать",
#             in_=openapi.IN_FORM
#         ),
#         openapi.Parameter(
#             name="files",
#             type=openapi.TYPE_FILE,
#             description="Файлы сообщения в формате\n[{\"имя файла\": \"байт-код\"}, ...]\nВ документации данного поля н"
#                         "ет так как swagger не поддерживает загрузку массива файлов в поле запроса",
#             in_=openapi.IN_FORM
#         ),
#     ],
# }

