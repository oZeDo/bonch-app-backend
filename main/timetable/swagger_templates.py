from drf_yasg import openapi
from rest_framework import status


TimetableRequest = {
    "method": "post",
    "operation_description": "Получить расписание:\n"
                             "- за день (info, type)\n"
                             "- за семестр (info, type, full)\n"
                             "- факультативов (info, type)\n"
                             "- в диапозане дат (info, type, from, to)\n"
                             "- экзаменов (info, type)",
    "request_body": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["info", "type"],
        properties={
            'info': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Данные',
                example="ИКТК-86"
            ),
            'type': openapi.Schema(
                type=openapi.TYPE_STRING,
                enum=["group", "tutor", "exam", "user_id"],
                description='Тип запрашиваемого расписания',
                example="group"
            ),
            'from': openapi.Schema(
                type=openapi.FORMAT_DATETIME,
                description='От',
                example="21-04-2020"
            ),
            'to': openapi.Schema(
                type=openapi.FORMAT_DATETIME,
                description='До',
                example="25-04-2020"
            ),
            'full': openapi.Schema(
                type=openapi.TYPE_BOOLEAN,
                enum=[True, False],
                description="Получить расписание за весь семестр",
                example=False
            ),
        }
    ),
    "responses": {status.HTTP_200_OK: openapi.Schema(
        type=openapi.TYPE_ARRAY,
        items=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'date': openapi.Schema(type=openapi.TYPE_STRING, example="2020-03-16 21:00:00.000000 +00:00"),
                'faculty': openapi.Schema(type=openapi.TYPE_STRING, example="РТС"),
                'group': openapi.Schema(type=openapi.TYPE_STRING, example="ИКТ-616"),
                'pair': openapi.Schema(type=openapi.TYPE_STRING, example="2"),
                'place': openapi.Schema(type=openapi.TYPE_STRING, example="300; Б22/1"),
                'subject': openapi.Schema(type=openapi.TYPE_STRING, example="Технология производства радиоэлектронных с"
                                                                            "редств"),
                'subject_type': openapi.Schema(type=openapi.TYPE_STRING, example="Лекция"),
                'time': openapi.Schema(type=openapi.TYPE_STRING, example="10:45-12:20"),
                'tutor': openapi.Schema(type=openapi.TYPE_STRING, example="Дёшина Н.О"),
                'tutor_full': openapi.Schema(type=openapi.TYPE_STRING, example="Дёшина Наталия Олеговна"),
                },
            )
        ),
    },
}

TutorRequest = {
    "method": "get",
    "operation_description": "Получить список преподавателей.",
    "manual_parameters": [
        openapi.Parameter(
            name="tp",
            type=openapi.TYPE_STRING,
            required=True,
            enum=["short", "long"],
            in_=openapi.IN_PATH
        )
    ],
    "responses": {
        status.HTTP_200_OK: openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_STRING, example="Дёшина Наталия Олеговна",
                )
            )
    },
}

GroupRequest = {
    "method": "get",
    "operation_description": "Получить список групп и факультетов",
    "responses": {
        status.HTTP_200_OK: openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_STRING, example="ИКСС\", \"ИКТК-86",
                ),
            )
        )
    },
}
