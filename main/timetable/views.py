from django.views.decorators.csrf import csrf_exempt
import datetime
from django.db.models import Q
from .models import Timetable, Group, Tutor
from .swagger_templates import TimetableRequest, TutorRequest, GroupRequest
from .serializers import TimetableSerializer
from django.utils.timezone import make_aware
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response


# Create your views here.
@csrf_exempt
@swagger_auto_schema(**TimetableRequest)
@api_view(["POST"])
def timetable(request):
    if request.data:
        type_ = request.data.get("type")
        info = request.data.get("info")
        from_ = request.data.get("from")
        to = request.data.get("to")
        full = request.data.get("full")
        if type_ is None and info is None:
            return Response({'detail': 'Пожалуйста предоставьте type или text.'}, status=status.HTTP_400_BAD_REQUEST)

        type_ = "tutor_full__contains" if type_ == "tutor" else type_

        if type_ == "user_id":
            query = {type_: request.user}
        elif type_ == "exam":
            query = (Q(subject_type='Экзамен') | Q(subject_type='Консультация') | Q(subject_type='Зачет')) & \
                       Q(group=info)
            i = Timetable.objects.filter(query).order_by('date')
            return Response(TimetableSerializer(i, many=True).data, status=status.HTTP_200_OK)
        elif type_ in ("group", "tutor_full__contains"):
            date = make_aware(datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0))
            query = {type_: info, "date__range": (date, date)}
            if from_ and to:
                from_ = datetime.datetime.strptime(from_, "%d-%m-%Y")
                to = datetime.datetime.strptime(to, "%d-%m-%Y")
                query["date__range"] = (from_, to)
            if full: del query["date__range"]
        else:
            return Response({'detail': 'Type указан неверно.'}, status=status.HTTP_400_BAD_REQUEST)
        i = Timetable.objects.filter(**query).order_by('date')
        return Response(TimetableSerializer(i, many=True).data, status=status.HTTP_200_OK)
    else:
        return Response({'detail': 'Параметры запроса пусты.'}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@swagger_auto_schema(**TutorRequest)
@api_view(["GET"])
def tutor(request, tp):
    i = [Tutor.objects.values_list("long", flat=True), Tutor.objects.values_list("short", flat=True)]
    if tp == "long":
        i = i[0]
    elif tp == "short":
        i = i[1]
    else:
        return Response({'detail': 'tp указан неверно.'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(i, status=status.HTTP_200_OK)


@csrf_exempt
@swagger_auto_schema(**GroupRequest)
@api_view(["GET"])
def group(request):
    i = Group.objects.values_list("faculty", "group")
    return Response(i, status=status.HTTP_200_OK)

