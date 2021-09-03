from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework import status, generics
from .serializers import EventSerializer, ProfileSerializer, FieldSerializer
from .models import Event, Profile, Field


# Create your views here.
class PagesPagination(PageNumberPagination):
    page_size = 10


class GetEventsView(generics.ListAPIView):
    queryset = Event.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = EventSerializer
    pagination_class = PagesPagination


class GetProfileView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ProfileSerializer


class CreateProfile(generics.CreateAPIView):
    queryset = Profile.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ProfileSerializer


class UpdateProfile(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ProfileSerializer


class GetForm(generics.RetrieveAPIView):
    queryset = Field.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = FieldSerializer


# @csrf_exempt
# @swagger_auto_schema(**EventFormRequest)
# @api_view(["GET"])
# @permission_classes((AllowAny,))
# def get_form(request, uuid):  # Собрать форму по указаному uuid
#     try:
#         data = []
#         event = Event.objects.get(uuid=uuid)
#         for field in Field.objects.filter(event=event).order_by("id"):
#             tmp = {
#                 "key": field.key,
#                 "name": field.name,
#                 "type": field.type,
#                 "required": field.required,
#                 "extra": []
#             }
#             try:
#                 for extra in Extra.objects.filter(field=field):
#                     tmp["extra"].append(extra.name)
#             except Extra.DoesNotExist:
#                 pass
#             data.append(tmp)
#
#     except Field.DoesNotExist or Event.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     return Response(data, status=status.HTTP_200_OK)
#
#
# @csrf_exempt
# @swagger_auto_schema(**EventsRequest)
# @api_view(["GET"])
# @permission_classes((AllowAny,))  # delete if not localhost
# def events(request):  # Список всех мер
#     event = Event.objects.all()
#     return Response(EventSerializer(event, many=True).data, status=status.HTTP_200_OK)
#
#
# @csrf_exempt
# @api_view(["POST", "PATCH", "GET", "DELETE"])
# @permission_classes((AllowAny,))  # delete if not localhost
# def form_answers(request, uuid):
#     try:
#         event = Event.objects.get(uuid=uuid)
#     except Event.DoesNotExist:
#         return Response({'detail': 'Мероприятие не найдено'}, status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == "POST":  # Записать ответы в бд [{key, answer}, ...]
#         if not request.data:
#             return Response({'detail': "Отсутствуют ответы на форму."}, status=status.HTTP_400_BAD_REQUEST)
#         if request.user.is_anonymous:
#             for i in request.data:
#                 Participant.objects.create(event=event, answer=i)
#         else:
#             for i in request.data:
#                 Participant.objects.create(event=event, answer=i, user=request.user)
#         return Response("Успех.", status=status.HTTP_201_CREATED)
#
#     elif request.method == "PATCH":  # Изменить ответы на существующую форму
#         if request.user.is_anonymous:
#             return Response({'detail': 'Метод запрещен для анонимных пользователей'},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         for i in Participant.objects.get(event=event, user=request.user).all():
#             i.answer = request.data
#             i.save()
#         return Response("Успех.", status=status.HTTP_200_OK)
#
#     elif request.method == "GET":  # Получить ответы на форму
#         if request.user.is_anonymous:
#             return Response({'detail': 'Метод запрещен для анонимных пользователей'},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         tmp = Participant.objects.get(user=request.user, event=event).all()
#         return Response(AnswerSerializer(tmp, many=True).data, status=status.HTTP_200_OK)
#
#     elif request.method == "DELETE":  # Удалить ответы на форму
#         if request.user.is_anonymous:
#             return Response({'detail': 'Метод запрещен для анонимных пользователей'},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#
#         Participant.objects.filter(event=event, user=request.user).delete()
#         return Response("Успех.", status=status.HTTP_200_OK)
#
#     else:
#         return Response({'detail': 'Метод запрещен'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#
