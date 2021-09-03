from django.contrib import admin
from .models import Event, Field, Extra, Participant, Profile
#
#
# # Register your models here.
# class EventFields(admin.ModelAdmin):
#     exclude = ["id"]
#     readonly_fields = ("uuid",)
#
#
# class Fields(admin.ModelAdmin):
#     exclude = ["id"]
#     readonly_fields = ("key",)
#     list_display = ('name', 'type', 'required', 'event')
#
#
admin.site.register(Event)
admin.site.register(Field)
admin.site.register(Profile)
admin.site.register(Extra)
admin.site.register(Participant)


