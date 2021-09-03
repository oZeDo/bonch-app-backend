from django.urls import path
from .views import GetEventsView, GetProfileView, CreateProfile, UpdateProfile, GetForm
# from .views import get_form, events, form_answers

urlpatterns = [
    # path('event/answers/<slug:uid>/', get_form),
    # path('event/form/<slug:uid>/', get_form),
    # path('event/<slug:uuid>/', get_form),    # Получить форму
    # path('event/answers/<slug:uuid>/', form_answers),   # Отправить/изменить/получить/удалить ответы на форму
    # path('event', events),    # Получить список всех мероприятий
    path('event/', GetEventsView.as_view(), name='events_list'),
    path('profile/<uuid:pk>', GetProfileView.as_view(), name='profile_retrieve'),
    path('profile/edit/<uuid:pk>', UpdateProfile.as_view(), name='profile_update'),
    path('profile/', CreateProfile.as_view(), name='profile_create'),
    path('event/form/<uuid:pk>', GetForm.as_view(), name='form_field_retrieve'),
]
