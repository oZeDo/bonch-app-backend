from django.urls import path
from .views import account, debt, mark, history, conversations, contacts

urlpatterns = (
    path('user/account', account),
    path('user/debt', debt),
    path('user/mark', mark),
    path('user/history', history),
    path('messages', conversations),
    path('messages/contacts', contacts)
)

