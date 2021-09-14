# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from timetable.models import Timetable, Group, Faculty
from .items import TimetableItem, GroupItem, FacultyItem
import datetime


class TimetablePipeline:
    def process_item(self, item, spider):
        if isinstance(item, TimetableItem):
            item["group"] = Group.objects.get(name=item["group"])
            item["faculty"] = item["group"].faculty
            obj, created = Timetable.objects.get_or_create(**item)
            if not created:
                obj.created = datetime.datetime.now()
                obj.save()
        elif isinstance(item, FacultyItem):
            obj, _ = Faculty.objects.get_or_create(**item)
        elif isinstance(item, GroupItem):
            item["faculty"] = Faculty.objects.get(name=item["faculty"])
            obj, _ = Group.objects.get_or_create(**item)
        return item


