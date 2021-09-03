from django import forms
from .models import Field


class EventForm(forms.ModelForm):
    class Meta:
        model = Field

