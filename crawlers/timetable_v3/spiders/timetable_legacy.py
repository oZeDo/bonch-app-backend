from ..items import FacultyItem, GroupItem, TimetableItem
from urllib.parse import urlencode
import datetime
import scrapy
import json


def time_corrector(day: str, week: str) -> datetime.date:
    """
    Считает дату пару прибавив к нулевой отметке недели и день недели
    :param day: День недели(1=понедельник..)
    :param week: Неделя на которой проводится пары
    :return: День когда будет пары
    """
    return day_zero + datetime.timedelta(days=7 * (int(week) - 1) + int(day) - 1)


URL = "https://cabinet.sut.ru/raspisanie_all_new"
day_zero = datetime.date(2021, 8, 30)


class TimetableSpider(scrapy.Spider):
    name = "timetable"
    start_urls = [URL]

    def parse(self, response):
        params = {
            "schet": response.css("select[id=schet] option[selected]::attr(value)").get(),  # Номер текущего семестра
            "choice": "1"
        }
        for i in response.css("select[id=faculty] option")[1:]:
            params["faculty"] = i.css("::attr(value)").get()
            yield FacultyItem(name=i.css("::text").get())
            # yield {i.css("::text").get(): }
            # i.css("::attr(value)").get()
            yield scrapy.FormRequest(url=URL, formdata=params, callback=self.parse_groups,
                                     cb_kwargs={"faculty": i.css("::text").get(), "semester": params["schet"]})

    def parse_groups(self, response, faculty, semester):
        params = {
            "schet": semester,
            "type_z": "1",  # Тип занятий: 1-обычные, 2-экзамены
        }
        groups = response.text.split(";")
        for group in groups[:-1]:
            group_id, group_name = group.split(",")
            yield GroupItem(faculty=faculty, name=group_name)
            params["group"] = group_id
            yield scrapy.Request(url=f"{URL}?{urlencode(params)}", callback=self.parse_timetable,
                                 cb_kwargs={"group": group_name, "faculty": faculty})

    def parse_timetable(self, response, group, faculty):
        for row in response.css("table.simple-little-table tbody tr")[1:-1]:  # Пропустить первый и последний tr таблицы
            data = {
                "group": group,
                "faculty": faculty,
                "pair": row.css("td[align]:not(div)::text").get().split()[0],
                "time": row.css("td[align]:not(div)::text").get().split()[1][1:-1]
            }
            for pair in row.css("td[align] div.pair"):
                for week in pair.css("small span.weeks::text").get()[1:-2].split(','):
                    data["subject"] = pair.css("span strong::text").get()
                    data["tutor"] = pair.css("i span.teacher::text").get()
                    data["tutor_fullname"] = pair.css("i span.teacher::attr(title)").get()
                    data["place"] = pair.css("span.aud::text").get()
                    if "*" in week:
                        data["subject_type"] = "Видеолекция"
                        week = week.replace("*", "")
                    else:
                        data["subject_type"] = pair.css("small span.type::text").get()[1:-1]  # "(Лекция)" -> "Лекция"
                    data["date"] = time_corrector(pair.css("::attr(weekday)").get(), week)
                    yield TimetableItem(**data)
