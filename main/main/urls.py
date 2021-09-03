"""DjangoAgain URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from core.views import login
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.generic import TemplateView

# Конфиг свагера
api_info = openapi.Info(
      title="BonchApp API",
      default_version='v1.3',
      contact=openapi.Contact(email="xkito@bonch.dev"),
   )

schema_view = get_schema_view(
    api_info,
    # Нужна для включения https в свагере
#    url='https://delta-axis.me/documentation',  # important
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
#    path('test/push', index),
#    url(r'^test/navigatorPush.service.js', (TemplateView.as_view(
#        template_name="navigatorPush.service.js",
#        content_type='application/javascript',
#    )), name='navigatorPush.service.js'),
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('api/', include('timetable.urls')),
    path('api/login', login),
    path('api/', include('scrapper.urls')),
    url(r'^documentation/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#    url(r'^silk/', include('silk.urls', namespace='silk')),
    path('api/activity/', include('activity.urls')),
]

# Доступ к файлам в локалке
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
