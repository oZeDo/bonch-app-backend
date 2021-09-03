from rest_framework import serializers

from .models import *


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ('id', 'user')


class DebtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Debt
        exclude = ('id', 'user')


class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        exclude = ('id', 'user')


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        exclude = ('id', 'user')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        exclude = ('user',)


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        exclude = ('id', 'user',)


class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        exclude = ('id', 'user')

