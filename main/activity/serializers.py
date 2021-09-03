from rest_framework import serializers
from .models import Event, Field, Extra, Participant, Profile
from rest_framework.serializers import ModelSerializer


class EventSerializer(ModelSerializer):
    creator_name = serializers.ReadOnlyField(source='creator.name')

    class Meta:
        model = Event
        fields = ["name", "picture", "description", "date",  "creator", "creator_name"]


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        exclude = ("id", "members")


class AnswerSerializer(ModelSerializer):
    class Meta:
        model = Participant
        fields = ["key", "answer"]


class FieldSerializer(ModelSerializer):
    class Meta:
        model = Field
        fields = '__all__'
