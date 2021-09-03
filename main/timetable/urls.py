from django.urls import path
from .views import timetable, tutor, group

urlpatterns = (
    path('timetable', timetable),
    path('timetable/tutor/<str:tp>', tutor),
    path('timetable/group', group),
)
