# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from scrapy_djangoitem import DjangoItem
from timetable.models import Faculty, Group, Timetable



class FacultyItem(DjangoItem):
    django_model = Faculty


class GroupItem(DjangoItem):
    django_model = Group


class TimetableItem(DjangoItem):
    django_model = Timetable
