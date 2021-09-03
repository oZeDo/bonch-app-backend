# Create your tasks here
from json.decoder import JSONDecodeError
from django.core.exceptions import ObjectDoesNotExist
from celery import shared_task
import requests
import datetime
import re
from bs4 import BeautifulSoup
from core.models import Cookie
from timetable.models import Tutor, Timetable, Group
from scrapper.models import *
from django.utils.timezone import make_aware
from django.conf import settings


start = datetime.datetime(2020, 8, 31)  # Воскресенье(?) прошлой недели перед первым учебным днем
start_week = 0  # нулевая неделя


def time_switch(time):
    return {
        "09:00-10:35": "1",
        "10:45-12:20": "2",
        "13:00-14:35": "3",
        "14:45-16:20": "4",
        "16:30-18:05": "5",
        "18:15-19:50": "6",
        "20:00-21:35": "7",
        "09:00-10:30": "Ф1",
        "10:30-12:00": "Ф2",
        "12:00-13:30": "Ф3",
        "13:30-15:00": "Ф4",
        "15:00-16:30": "Ф5",
    }[time]


def request(date='', type_z='', fac='', number='', credit=False):
    url = "https://cabinet.sut.ru/raspisanie_all_new"
    data_ = {
        "schet": date,
        "type_z": type_z,
        "faculty": fac,
        "group": number
    }
    if credit: data_["rasp_zach"] = True
    resp = requests.session()
    resp = resp.post(url=url, data=data_, headers=settings.HEADER)
    soup = BeautifulSoup(resp.content, "lxml")
    return soup


def time_corrector(day, week):
    return start + datetime.timedelta(days=7 * (int(week) - 1) + day)


def tutors_splitter(dict_):
    if dict_.get("tutor_full"):
        if ";" in dict_["tutor_full"]:
            tmp1 = dict_["tutor_full"].split(";")
            tmp2 = [x for x in re.split(r'(.*?\s.*?)\s', dict_["tutor"]) if x]

            for array in [tmp1, tmp2]:
                for pos, val in enumerate(array):
                    array[pos] = val.strip()
                    if val[-1] == '.':
                        array[pos] = val[:-1]

            tmp1.sort()
            tmp2.sort()
            assert len(tmp2) == len(tmp1), "Tutors are not equal"
            return tmp1, tmp2
        else:
            return [dict_["tutor_full"]], [dict_["tutor"]]
    return None, None


def pair_fixer(pair):
    if len(pair) == 2:
        return {
            "83": "Ф1",
            "84": "Ф2",
            "85": "Ф3",
            "86": "Ф4",
            "87": "Ф5",
        }[pair]
    return pair


@shared_task
def debt(user_id):
    user = User.objects.get(pk=user_id)
    url = "https://lk.sut.ru/cabinet/project/cabinet/forms/dolg.php"
    cookies = Cookie.objects.get(user=user)
    cookies = {"uid": cookies.uid, "miden": cookies.miden}
    resp = requests.post(url=url, cookies=cookies, headers=settings.HEADER)

    soup = BeautifulSoup(resp.content, "lxml")
    try:
        for i in soup.find("table", class_="simple-little-table").find("tbody").find_all("tr")[1:]:
            data = {
                "course": i.find_all("td")[0].text,
                "semester": i.find_all("td")[1].text,
                "subject": i.find_all("td")[2].text,
                "subject_type": i.find_all("td")[4].text,
                "user": user
            }
            obj, created = Debt.objects.get_or_create(**data)
            if created:
                obj.save()
    except AttributeError:
        pass


@shared_task
def account(user_id):
    user = User.objects.get(pk=user_id)
    url = "https://lk.sut.ru/cabinet/project/cabinet/forms/profil.php"
    cookies = Cookie.objects.get(user=user)
    cookies = {"uid": cookies.uid, "miden": cookies.miden}
    resp = requests.post(url=url, cookies=cookies, headers=settings.HEADER)
    soup = BeautifulSoup(resp.content, "lxml")

    body = soup.find_all("table", class_="profil")
    data = {
        "fullname": body[0].find_all("tr")[1].find("td").text,
        "birth_date": make_aware(datetime.datetime.strptime(body[0].find_all("tr")[2].find("td").text.strip(),
                                                            "%d.%m.%Y")),
        "faculty": body[1].find_all("tr")[1].find("td").text,
        "group": body[1].find_all("tr")[6].find("td").text,
        "user": user,
        "headman": False
    }
    try:
        data["course"] = int(body[1].find_all("tr")[7].find("td").text)
    except ValueError:
        data["course"] = int(body[1].find_all("tr")[8].find("td").text)
        data["headman"] = True

    obj, created = Account.objects.get_or_create(**data)
    if created:
        obj.save()


@shared_task
def mark(user_id):
    user = User.objects.get(pk=user_id)
    url = "https://lk.sut.ru/cabinet/project/cabinet/forms/zachetka.php"
    cookies = Cookie.objects.get(user=user)
    cookies = {"uid": cookies.uid, "miden": cookies.miden}
    resp = requests.post(url=url, cookies=cookies, headers=settings.HEADER)
    soup = BeautifulSoup(resp.content, "lxml")

    for i in soup.find("table", class_="simple-little-table").find("tbody").find_all("tr")[2:]:
        data = {
            "course": i.find_all("td")[0].text,
            "semester": i.find_all("td")[1].text,
            "subject": i.find_all("td")[2].text,
            "user": user
        }
        if i.find_all("td")[4].text:
            data["mark"] = i.find_all("td")[4].text
        else:
            data["mark"] = i.find_all("td")[5].text
        obj, created = Mark.objects.get_or_create(**data)
        if created:
            obj.save()


@shared_task
def history(user_id):
    user = User.objects.get(pk=user_id)
    url = "https://lk.sut.ru/cabinet/project/cabinet/forms/fakultativ_history.php"
    cookies = Cookie.objects.get(user=user)
    cookies = {"uid": cookies.uid, "miden": cookies.miden}
    resp = requests.post(url=url, cookies=cookies, headers=settings.HEADER)
    soup = BeautifulSoup(resp.content, "lxml")

    try:
        for i in soup.find("table", class_="simple-little-table").find("tbody").find_all("tr")[1:]:
            data = {
                "subject": i.find_all("td")[0].text,
                "status": i.find_all("td")[3].text,
                "mark": i.find_all("td")[6].text,
                "user": user
            }
            obj, created = History.objects.get_or_create(**data)
            if created:
                obj.save()
    except AttributeError:
        pass


@shared_task
def elective(user_id):
    user = User.objects.get(pk=user_id)
    url = "https://cabs.itut.ru/cabinet/project/cabinet/forms/fakultativ_rasp.php"
    url2 = "https://lk.sut.ru/cabinet/project/cabinet/forms/raspisanie.php?week="

    cookies = Cookie.objects.get(user=user)
    cookies = {"uid": cookies.uid, "miden": cookies.miden}
    resp = requests.post(url=url, cookies=cookies, headers=settings.HEADER)
    soup = BeautifulSoup(resp.content, "lxml")

    data = {}
    try:
        constant = (len(soup.find("table", class_="simple-little-table").find_all("tr")) - 1) // 16
        for j in range(constant):
            temp1, temp2 = None, None
            for i in soup.find("table", class_="simple-little-table").find_all("tr")[
                     j * 18 + 1 + j:(j + 1) * 18 + 2 + j]:
                if i.find("b"):
                    data["subject"] = i.text
                    continue
                if i.find("td"):
                    tmp = datetime.datetime.strptime(i.find_all("td")[0].text, "%d-%m-%Y")
                    data["date"] = make_aware(tmp)
                    data["time"] = i.find_all("td")[1].text
                    data["place"] = i.find_all("td")[2].text
                    data["subject_type"] = "Факультатив"
                    data["pair"] = time_switch(data["time"])
                    data["user"] = user
                    if temp1 and temp2:
                        data["tutor"] = temp1
                        data["tutor_full"] = temp2
                    else:
                        week = (tmp - start).days // 7 + 1 + start_week
                        resp2 = requests.post(url=url2 + str(week), cookies=cookies, headers=settings.HEADER)
                        soup2 = BeautifulSoup(resp2.content, "lxml")
                        for s in soup2.find_all("tr"):
                            fac = s.find("b")
                            if fac:
                                if "Факультатив: " + data["subject"] in fac.text:
                                    temp1 = s.find_all("td")[3].text[:-1]
                                    temp2 = Tutor.objects.get(short=temp1).long
                                    data["tutor"] = temp1
                                    data["tutor_full"] = temp2
                                    break
                obj, created = Timetable.objects.get_or_create(**data)
                if created:
                    obj.save()
    except AttributeError:
        pass


def read_file(file_id, soupp, cookies, is_read=True):
    url = "https://lk.sut.ru/cabinet/project/cabinet/forms/files_group_pr.php"
    if not is_read:
        requests.post(url=url, data={"read": "", "idread": file_id}, cookies=cookies, headers=settings.HEADER)

    temp = soupp.find("table", class_="simple-little-table").find("tbody").find("tr", attrs={"id": file_id})

    temp = temp.find_all("td")[3].text.replace("\r\n", " ")
    while '  ' in temp:
        temp = temp.replace('  ', ' ')
    return temp


def read_message(message_id, cookies):
    url = "https://lk.sut.ru/cabinet/project/cabinet/forms/sendto2.php"
    temp = requests.post(url=url, data={"id": int(message_id), "prosmotr": ""}, cookies=cookies,
                         headers=settings.HEADER)
    try:
        temp = temp.json()["annotation"]
        temp = re.sub('<[^<]+?>', '', temp.replace("\r\n", " ").replace("<br><br>", "<br>")
                      .replace("<br>", "\n").replace("&nbsp;", " ")
                      )
        while '  ' in temp:
            temp = temp.replace('  ', ' ')
        temp = temp.rstrip("\n")
        return temp
    except JSONDecodeError:
        return ""


@shared_task()
def message_constructor(params, user_id, fullname, cookies, type_="in"):
    url = "https://lk.sut.ru/cabinet/project/cabinet/forms/message.php"
    user = User.objects.get(pk=user_id)
    resp = requests.post(url=url, data=params, cookies=cookies, headers=settings.HEADER)
    soup = BeautifulSoup(resp.content, "lxml")

    for j in soup.find("table", class_="simple-little-table").find("tbody").find_all("tr", id=re.compile("^tr_")):
        tags = j.find_all("td")
        unread_flag = j.get("style")
        if tags[0].text == "Сообщений не найдено":
            continue
        elif tags[3].text == fullname or len(tags[3].text) == 0:
            continue
        else:
            try:
                message = Message.objects.get(user=user, message_id=int(j["id"][3:]))
                if unread_flag:
                    continue
                elif message.read:
                    continue
                else:
                    message.text = read_message(message.message_id, cookies)
                    message.read = True
                    message.addressed_id = message.message_id
                    message.save()
                    continue
            except ObjectDoesNotExist:
                tmp = datetime.datetime.strptime(tags[0].text, "%d-%m-%Y %H:%M:%S")
                tmp = make_aware(tmp)
                data = {
                    "user": user,
                    "date": tmp,
                    "subject": tags[1].text.strip(),
                    "destination": tags[3].text.replace(" (сотрудник/преподаватель)", ""),
                    "message_id": int(j["id"][3:]),
                    "type": type_
                }

                #print(data)

                if unread_flag:
                    if data["type"] == "in":
                        data["text"] = None
                        data["read"] = False
                        data["addressed_id"] = None
                    else:
                        data["text"] = read_message(data["message_id"], cookies)
                        data["read"] = False
                        data["addressed_id"] = data["message_id"]
                else:
                    data["text"] = read_message(data["message_id"], cookies)
                    data["read"] = True
                    data["addressed_id"] = data["message_id"]

                obj = Message.objects.create(**data)
                obj.save()

                for a in tags[2].find_all(href=True):
                    File.objects.create(name=a.text, url="https://lk.sut.ru/" + a["href"], message=obj).save()


@shared_task()
def message(user_id):
    url = "https://lk.sut.ru/cabinet/project/cabinet/forms/message.php"
    params = {}
    user = User.objects.get(pk=user_id)
    cookies = Cookie.objects.get(user=user)
    fullname = Account.objects.get(user=user).fullname
    cookies = {"uid": cookies.uid, "miden": cookies.miden}
    message_constructor({"search": "", "notread": 1}, user.id, fullname, cookies)

    for s in ["in", "out", "del"]:
        params["type"] = s
        resp = requests.post(url=url, data=params, cookies=cookies, headers=settings.HEADER)
        soup = BeautifulSoup(resp.content, "lxml")
        try:
            last_page = soup.find("span", id="table_mes").find("center").find_all("a")[-1]["onclick"]
            pages = int(re.search(r'[\d]+', last_page).group(0))
        except IndexError:
            pages = 1

        for i in range(1, pages + 1):
            params["page"] = i
            if settings.NO_DOCKER:
                message_constructor(params, user.id, fullname, cookies, s)
            else:
                message_constructor.delay(params, user.id, fullname, cookies, s)


@shared_task()
def contacts(user_id):
    user = User.objects.get(pk=user_id)
    cookies = Cookie.objects.get(user=user)
    cookies = {"uid": cookies.uid, "miden": cookies.miden}
    url = "https://lk.sut.ru/cabinet/project/cabinet/forms/message_create_stud.php"

    resp = requests.post(url=url, cookies=cookies, headers=settings.HEADER)
    soup = BeautifulSoup(resp.content, "lxml")
    for i in soup.find("select", attrs={"name": "adresat"}).find_all("option"):
        if int(i["value"]) != 0:
            obj, created = Contact.objects.get_or_create(send_to=int(i["value"]), user=user, name=i.text)
            if created:
                obj.save()


@shared_task
def files(user_id):
    user = User.objects.get(pk=user_id)
    cookies = Cookie.objects.get(user=user)
    cookies = {"uid": cookies.uid, "miden": cookies.miden}
    url = "https://lk.sut.ru/cabinet/project/cabinet/forms/files_group_pr.php"
    resp = requests.post(url=url, cookies=cookies, headers=settings.HEADER)
    soup = BeautifulSoup(resp.content, "lxml")

    for i in soup.find("table", class_="simple-little-table").find("tbody").find_all("tr"):
        tmp = make_aware(datetime.datetime.strptime(i.find_all("td")[1].text, "%d-%m-%Y %H:%M:%S"))
        data = {
            "user": user,
            "date": tmp,
            "subject": i.find_all("td")[2].text.strip(),
            "destination": i.find_all("td")[0].text,
            "message_id": int(i["id"]),
            "type": "in",
        }
        if i.get("style") == "font-weight: bold;":
            data["read"] = False
            data["text"] = None
            data["addressed_id"] = None
        else:
            data["read"] = True
            data["text"] = read_file(data["message_id"], soup, cookies)

        obj_, created = Message.objects.get_or_create(**data)
        if created:
            obj_.save()

        for a in i.find_all("td")[4].find_all(href=True):
            obj, created = File.objects.get_or_create(name=a.text, url="https://lk.sut.ru/" + a["href"],
                                                      message=obj_)
            if created:
                obj.save()


@shared_task
def update_cookie():
    url = "https://lk.sut.ru/cabinet/lib/updatesession.php"
    cookies = Cookie.objects.all()
    for cookie in cookies:
        cookie_data = {"uid": cookie.uid, "miden": cookie.miden}
        requests.post(url=url, cookies=cookie_data, headers=settings.HEADER)


@shared_task()
def parse_timetable():
    data = {}
    groups = []
    semester_date = []
    all_groups = Timetable.objects.values_list('group').distinct()  # In database

    for i in request().find("select", id="schet").find_all("option"):
        if i.get("value") != "0":
            semester_date.append(i.get("value"))

    faculty = {}
    for i in request(semester_date[0], "1").find("select", id="faculty").find_all("option"):
        if i.get("value") != "0":
            faculty[i.text] = {"id": i.get("value"), "groups": {}}

    for _, j in faculty.items():
        for s in request(semester_date[0], "1", j["id"]).find("select", id="group").find_all("option"):
            if s.get("value") != "0":
                j["groups"][s.get("value")] = s.text
                if s.text not in all_groups:
                    Timetable.objects.filter(group=s.text).delete()

    for i, j in faculty.items():
        for k, l in j["groups"].items():
            groups.append({"faculty": i, "group": l})

    #Group.objects.all().delete()
    Group.objects.bulk_create([Group(**group) for group in groups])

    for fac_name, fac_items in faculty.items():
        for group_id, group_name in fac_items["groups"].items():
            Timetable.objects.filter(group=group_name).delete()
            # Занятия
            for i in request(semester_date[0], "1", fac_items["id"], group_id).find("table").find_all("tr")[1:-1]:
                data["group"] = group_name
                data["faculty"] = fac_name
                k = i.find("td")
                if k:
                    if len(k.text) > 0:
                        if (k.text[0] != "Ф" and int(k.text[0]) == 7) or k.text == "20:00-21:30":
                            data["pair"], data["time"] = "7", "20:00-21:35"
                        else:
                            data["time"], data["pair"] = k.text.split()[1][1:-1], k.text.split()[0]
                    elif len(k.text) == 0:
                        data["pair"], data["time"] = "6", "18:15-19:50"
                for k, j in enumerate(i.find_all("td")[1:], start=1):
                    for s in j.find_all("div", class_="pair"):
                        data["subject"] = s.find("strong").text
                        data["subject_type"] = s.find("span", class_="type").text[1:-1]
                        weeks = s.find("span", class_="weeks").text[1:-2].split(',')
                        if s.find("span", class_="aud"):
                            data["place"] = s.find("span", class_="aud").text[7:]
                        else:
                            data["place"] = None

                        if s.find("span", class_="teacher"):
                            data["tutor"] = s.find("span", class_="teacher").text[:-2]
                            data["tutor_full"] = s.find("span", class_="teacher").get("title")[:-2].split()
                            if data["tutor_full"][-1] == "-" and len(data["tutor_full"]) > 3:
                                del data["tutor_full"][-1]
                            data["tutor_full"] = ' '.join(data["tutor_full"])
                        else:
                            data["tutor"], data["tutor_full"] = None, None
                        if not data["tutor"] and data["tutor_full"]:
                            tmp = data["tutor_full"].split()
                            data["tutor"] = '{} {:.1}.{:.1}'.format(*tmp)

                        tutor_full_tmp, tutor_tmp = tutors_splitter(data)

                        for w in weeks:
                            if "*" in w.strip():
                                w = w.replace("*", "")
                                data["subject_type"] = "Видеолекция"
                            data["date"] = make_aware(time_corrector(k, w))

                            if tutor_full_tmp:
                                for num, name in enumerate(tutor_tmp):
                                    data["tutor_full"] = tutor_full_tmp[num]
                                    if name.isupper():  # Костыль для записи АЛЕКСЕЕВА О.М
                                        temp = name.split()
                                        name = "{0} {1}".format(temp[0].capitalize(), temp[1])
                                    # Костыль для записи Киселева А.В
                                    name = "Киселёва А.В" if name == "Киселева А.В" else name
                                    data["tutor"] = name
                                    Timetable.objects.create(**data)
                            else:
                                Timetable.objects.create(**data)
            data.clear()

            # Зачеты
            j = request(semester_date[0], "1", fac_items["id"], group_id, True).find("tbody")
            if j:
                data["group"] = group_name
                data["faculty"] = fac_name
                for i in j.find_all("tr")[1:]:
                    k = i.find_all("td")
                    temp_ = datetime.datetime.strptime(re.sub(r"[а-яА-Я a-zA-Z]", "", k[0].text), "%d.%m.%Y")
                    data["date"] = make_aware(temp_)
                    data["time"], data["pair"] = k[1].text.split()[1][1:-1], pair_fixer(k[1].text.split()[0])
                    data["subject_type"] = k[2].text
                    data["subject"] = k[3].find("span").text
                    data["tutor_full"] = k[4].find("span").text
                    if len(data["tutor_full"]) == 0:
                        data["tutor_full"] = None
                        data["tutor"] = None
                    else:
                        if ";" in data["tutor_full"]:
                            tmp = data["tutor_full"].split(";")
                            tmp[0], tmp[1] = tmp[0].split(), tmp[1].split()
                            if len(tmp[0]) > 3 or len(tmp[1]) > 3:
                                tmp[0], tmp[1] = tmp[0][:3], tmp[0][:3]
                            tmp[0] = '{} {:.1}.{:.1}'.format(*tmp[0])
                            tmp[1] = '{} {:.1}.{:.1}'.format(*tmp[1])
                            data["tutor"] = ' '.join(tmp)
                        else:
                            tmp = data["tutor_full"].split()
                            if tmp[-1] == '-' and len(tmp) > 3:
                                del tmp[-1]
                            if len(tmp) == 2:
                                tmp.append("-")
                            elif len(tmp) % 3 == 0:
                                tmp = tmp[:3]
                            data["tutor_full"] = " ".join(tmp)
                            data["tutor"] = '{} {:.1}.{:.1}'.format(*tmp)
                    data["place"] = k[5].find("span").text

                    tutor_full_tmp, tutor_tmp = tutors_splitter(data)

                    if tutor_full_tmp:
                        for num, name in enumerate(tutor_tmp):
                            data["tutor_full"] = tutor_full_tmp[num]
                            data["tutor"] = name
                            Timetable.objects.create(**data)
                    else:
                        Timetable.objects.create(**data)
            data.clear()

            # Экзамены
            # for i in request(semester_date[0], "2", fac_items["id"], group_id).find("table").find_all("tr")[1:-1]:
            #     pass

