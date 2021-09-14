import asyncio
import httpx

import requests
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RegisterSerializer, MyTokenObtainPairSerializer
from .swagger_templates import LoginRequest
from django.views.decorators.csrf import csrf_exempt
from .models import Cookie, User
from scrapper.forms import UserCreationForm
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status, generics
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from scrapper.models import *
from scrapper.tasks import debt, account, elective, history, mark, files, message
import six
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.conf import settings


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


@permission_classes((AllowAny,))
def index(request):
    return render(request, 'index.html')


async def bonch_authorize(username, password):
    url = "https://lk.sut.ru/cabinet/"
    data = {
        "users": username,
        "parole": password,
    }
    async with httpx.AsyncClient() as client:
        cookies = await client.get(url=url, headers=settings.HEADER).cookies
        resp = await client.post(url="https://lk.sut.ru/cabinet/lib/autentificationok.php", data=data, cookies=cookies,
                                 headers=settings.HEADER)
        if resp.content.decode() == "1":
            cookies = cookies.get_dict()
            await client.get(url="https://lk.sut.ru/cabinet/?login=yes", cookies=cookies, headers=settings.HEADER)
            return cookies
        return None


@csrf_exempt
@swagger_auto_schema(**LoginRequest)
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'detail': 'Пожалуйста предоставьте username и password.'},
                        status=status.HTTP_400_BAD_REQUEST)
    username = username.lower()
    cookies = asyncio.run(bonch_authorize(username, password))
    if cookies:
        try:
            user = User.objects.get(email=username)
        except ObjectDoesNotExist:
            user = User.objects.create(email=username)
            user.set_password(password)
            user.save()

        obj, _ = Cookie.objects.get_or_create(user=user)
        obj.miden = cookies["miden"]
        obj.uid = cookies["uid"]
        obj.save()

        account(user.id)
        if settings.NO_DOCKER:
            debt(user.id)
            history(user.id)
            elective(user.id)
            message(user.id)
            files(user.id)
            mark(user.id)
        else:
            debt.delay(user.id)
            history.delay(user.id)
            elective.delay(user.id)
            message.delay(user.id)
            files.delay(user.id)
            mark.delay(user.id)

    else:
        return Response({'detail': 'Неверные учетные данные.'},
                        status=status.HTTP_401_UNAUTHORIZED)
    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=status.HTTP_200_OK)

# class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
#     def make_hash_value(self, user, timestamp):
#         return (
#             six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.signup.signup_confirmation)
#         )
#
#
# account_activation_token = AccountActivationTokenGenerator()
# @csrf_exempt
# def signup(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST, request.FILES)
#         if form.is_valid():
#             user = form.save()
#             user.refresh_from_db()
#             user.profile.description = form.cleaned_data.get('description')
#             user.profile.icon = form.cleaned_data.get("image")
#             user.is_active = False
#             user.save()
#             current_site = get_current_site(request)
#             subject = 'Please Activate Your Account'
#             # load a template like get_template()
#             # and calls its render() method immediately.
#             message = render_to_string('activation_request.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 # method will generate a hash value with user related data
#                 'token': account_activation_token.make_token(user),
#             })
#             user.email_user(subject, message)
#             return redirect('activation_sent')
#         else:
#             print(form.is_valid())
#     else:
#         form = UserCreationForm()
#     return render(request, 'signup.html', {'form': form})
#
#
# @csrf_exempt
# def activation_sent_view(request):
#     return render(request, 'activation_sent.html')
#
#
# @csrf_exempt
# def activate(request, uidb64, token):
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     # checking if the user exists, if the token is valid.
#     if user is not None and account_activation_token.check_token(user, token):
#         # if valid set active true
#         user.is_active = True
#         # set signup_confirmation true
#         user.profile.signup_confirmation = True
#         user.save()
#         return redirect('admin_activation.html')
#     else:
#         return render('404.html')


# class UserRegistrationView(CreateAPIView):
#     serializer_class = UserRegistrationSerializer
#     permission_classes = (AllowAny,)
#
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         status_code = status.HTTP_201_CREATED
#         response = {
#             'success': 'True',
#             'status code': status_code,
#             'message': 'User registered  successfully',
#         }
#
#         return Response(response, status=status_code)


# class UserLoginView(RetrieveAPIView):
#
#     permission_classes = (AllowAny,)
#     serializer_class = UserLoginSerializer
#
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         response = {
#             'success': 'True',
#             'status code': status.HTTP_200_OK,
#             'message': 'Пользователь успешно авторизовался.',
#             'token': serializer.data['token'],
#             }
#         status_code = status.HTTP_200_OK
#
#         return Response(response, status=status_code)


# @csrf_exempt
# @permission_classes((AllowAny,))
# def register(request, success_url=None,
#              #form_class=RegistrationForm,
#              form_class=RegistrationFormUniqueEmail,
#              profile_callback=None,
#              template_name='registration/registration_form.html',
#              extra_context=None):
#     # profile = Profile.objects.get(user=request.user)
#     return render(request, 'form.html')
    # return render(request, 'profile.html', {"user": request.user, "profile": profile})


#  Обновление токена
# utc_now = datetime.datetime.utcnow()
# if not created:
#     if token.created < utc_now - datetime.timedelta(hours=24):
#         token.delete()
#         token = Token.objects.create(user=serializer.object['user'])
#     # update the created time of the token to keep it valid
#     token.created = datetime.datetime.utcnow()
#     token.save()
