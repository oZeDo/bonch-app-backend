import io
from pprint import pprint
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FileUploadParser, JSONParser
from rest_framework.response import Response
from core.models import Cookie
from .serializers import *
from .swagger_templates import *
import requests
import collections
from django.conf import settings


# Create your views here.
@csrf_exempt
@swagger_auto_schema(**AccountRequest)
@api_view(["GET"])
def account(request):
    i = Account.objects.get(user=request.user)
    return Response(AccountSerializer(i).data, status=status.HTTP_200_OK)


@csrf_exempt
@swagger_auto_schema(**MarkRequest)
@api_view(["GET"])
def mark(request):
    i = Mark.objects.filter(user=request.user).order_by("id")
    return Response(MarkSerializer(i, many=True).data, status=status.HTTP_200_OK)


@csrf_exempt
@swagger_auto_schema(**DebtRequest)
@api_view(["GET"])
def debt(request):
    i = Debt.objects.filter(user=request.user).order_by("id")
    return Response(DebtSerializer(i, many=True).data, status=status.HTTP_200_OK)


@csrf_exempt
@swagger_auto_schema(**HistoryRequest)
@api_view(["GET"])
def history(request):
    i = History.objects.filter(user=request.user).order_by("id")
    return Response(HistorySerializer(i, many=True).data, status=status.HTTP_200_OK)


@csrf_exempt
@swagger_auto_schema(**ContactRequest)
@api_view(["GET"])
def contacts(request):
    i = Contact.objects.filter(user=request.user).order_by("id")
    return Response(ContactSerializer(i, many=True).data, status=status.HTTP_200_OK)


@csrf_exempt
@swagger_auto_schema(**MessageSendRequest)
@swagger_auto_schema(**ConversationsRequest)
@swagger_auto_schema(**MessageDeleteRequest)
@api_view(["GET", "DELETE", "POST"])
def conversations(request):
    if request.method == 'GET':
        # d = collections.defaultdict(dict)
        # for name, subject in Message.objects.filter(user=request.user).values_list("destination", "subject").distinct():
        #     tmp = Message.objects.filter(user=request.user, destination=name, subject=subject)
        #     d[name][subject] = tmp.values("id", "date", "text", "read", "addressed_id", "type")
        #     for j in d[name][subject]:
        #         j["files"] = File.objects.filter(message_id=j["id"]).values("name", "url")
        # d = dict(d)
        d = MessageSerializer(Message.objects.filter(user=request.user).order_by("-date"), many=True).data
        for j in d:
            j["files"] = File.objects.filter(message_id=j["id"]).values("name", "url")
            del j["id"]
        return Response(d, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        url = "https://lk.sut.ru/cabinet/project/cabinet/forms/message.php"
        cookies = Cookie.objects.get(user=request.user)
        cookies = {"uid": cookies.uid, "miden": cookies.miden}
        ids = request.data.get("message")
        i = Message.objects.filter(user=request.user, message_id__in=ids).values_list("message_id", flat=True)
        print(i)
        requests.post(url=url, data={"id_del[]": i, "delmes": 2}, cookies=cookies, headers=settings.HEADER)
        return Response("Успех.", status=status.HTTP_200_OK)
    elif request.method == 'POST':
        idinfo = 0
        upload = "https://lk.sut.ru/cabinet/project/cabinet/forms/message_create_stud.php"
        url = "https://lk.sut.ru/cabinet/project/cabinet/forms/message.php"
        text = request.data.get("text")
        message_type = request.data.get("message_type")
        item = request.data.get("item")
        files = request.data.get("files")
        subject = request.data.get("subject")

        if files:
            try:
                files = {
                    files.name: files.read(),
                }
            except AttributeError:
                pass

        cookies = Cookie.objects.get(user=request.user)
        cookies = {"uid": cookies.uid, "miden": cookies.miden}
        if files:
            for name, byte_string in files.items():
                file = io.BytesIO(byte_string)
                file.name = name
                r = requests.post(upload, cookies=cookies, data={"id": idinfo, "upload": ""}, files={"userfile": file},
                                  headers=settings.HEADER)
                if idinfo == 0:
                    for k in r.content.decode("windows-1251")[30:-9].split(";"):
                        if "data.idinfo" in k:
                            idinfo = int(k.split("=")[1].strip()[1:-1])

        if message_type == "new":
            requests.post(upload, cookies=cookies, data={
                "adresat": item,
                "idinfo": idinfo,
                "mes": text,
                "title": subject
            }, headers=settings.HEADER)
            return Response("Успех.", status=status.HTTP_200_OK)
        elif message_type == "reply":
            requests.post(url, cookies=cookies, data={
                "item": item,
                "idinfo": idinfo,
                "mes_otvet": text
            }, headers=settings.HEADER)
            return Response("Успех.", status=status.HTTP_200_OK)

