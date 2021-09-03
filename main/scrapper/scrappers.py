import requests
import datetime
import time
import re
from bs4 import BeautifulSoup
from .tasks import debt, account, mark, history, elective
start = datetime.datetime(2020, 9, 1)  # Воскресенье(?) прошлой недели перед первым учебным днем
start_week = 1  # нулевая неделя

"""
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


def read_file(file_id, soupp, cookies, is_read=True):
    url = "https://lk.sut.ru/cabinet/project/cabinet/forms/files_group_pr.php"
    if not is_read:
        requests.post(url=url, data={"read": "", "idread": file_id}, cookies=cookies)

    temp = soupp.find("table", class_="simple-little-table").find("tbody").find("tr", attrs={"id": file_id})

    temp = temp.find_all("td")[3].text.replace("\r\n", " ")
    while '  ' in temp:
        temp = temp.replace('  ', ' ')
    return temp


def read_message(message_id, cookies):
    url = "https://lk.sut.ru/cabinet/project/cabinet/forms/sendto2.php"
    temp = requests.post(url=url, data={"id": int(message_id), "prosmotr": ""}, cookies=cookies).json()["annotation"]
    temp = re.sub('<[^<]+?>', '', temp.replace("\r\n", " ").replace("<br><br>", "<br>")
                  .replace("<br>", "\n").replace("&nbsp;", " ")
                  )
    while '  ' in temp:
        temp = temp.replace('  ', ' ')
    temp = temp.rstrip("\n")
    return temp


# messages
def message(user):
    x = time.time()
    cookies = Cookie.objects.get(user=user)
    cookies = {"uid": cookies.uid, "miden": cookies.miden}
    url = "https://lk.sut.ru/cabinet/project/cabinet/forms/message.php"
    params = {}

    for s in ["in", "out", "del"]:

        params["type"] = s
        resp = requests.post(url=url, data=params, cookies=cookies)
        soup = BeautifulSoup(resp.content, "lxml")

        try:
            pages = re.search(r"\d", soup.find("span", id="table_mes")
                              .find("center").find_all("a")[-1]["onclick"]).group(0)
        except IndexError:
            pages = 1

        for i in range(1, int(pages) + 1):
            params["page"] = i
            resp = requests.post(url=url, data=params, cookies=cookies)
            soup = BeautifulSoup(resp.content, "lxml")

            for j in soup.find("table", class_="simple-little-table").find("tbody").find_all("tr"):
                if j.td.text == "Сообщений не найдено":
                    break
                if j.has_attr("id") and j["id"][:3] == "tr_":
                    tmp = make_aware(datetime.datetime.strptime(j.find_all("td")[0].text, "%d-%m-%Y %H:%M:%S"))
                    data = {
                        "user": user,
                        "date": tmp,
                        "subject": j.find_all("td")[1].text.strip(),
                        "destination": j.find_all("td")[3].text.replace(" (сотрудник/преподаватель)", ""),
                        "message_id": int(j["id"][3:]),
                        "type": s
                    }

                    if j.get("style") and s == "in":
                        data["read"] = False
                        data["text"] = None
                        data["addressed_id"] = None
                    elif j.get("style") and s == "out":
                        data["text"] = read_message(data["message_id"], cookies)
                        data["read"] = False
                        data["addressed_id"] = data["message_id"]
                    else:
                        data["text"] = read_message(data["message_id"], cookies)
                        data["read"] = True
                        data["addressed_id"] = data["message_id"]

                    data["deleted"] = True if s == "del" else False

                    obj_, created = Message.objects.get_or_create(**data)
                    if created:
                       obj_.save()

                    for a in j.find_all("td")[2].find_all(href=True):
                        obj, created = File.objects.get_or_create(name=a.text, url="https://lk.sut.ru/" + a["href"],
                                                                  message=obj_)
                        if created:
                            obj.save()

    url = "https://lk.sut.ru/cabinet/project/cabinet/forms/message_create_stud.php"
    resp = requests.post(url=url, cookies=cookies)
    soup = BeautifulSoup(resp.content, "lxml")
    for i in soup.find("select", attrs={"name": "adresat"}).find_all("option"):
        if int(i["value"]) != 0:
            obj, created = Contact.objects.get_or_create(send_to=int(i["value"]), user=user, name=i.text)
            if created:
                obj.save()
    print("messages", time.time() - x)


def files(user):
    x = time.time()
    cookies = Cookie.objects.get(user=user)
    cookies = {"uid": cookies.uid, "miden": cookies.miden}
    url = "https://lk.sut.ru/cabinet/project/cabinet/forms/files_group_pr.php"
    resp = requests.post(url=url, cookies=cookies)
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

    print('files', time.time() - x)
"""


def get_all(user):
    print("started")
    x = time.time()
    print(x)
    print("first worker started task")
    account.delay(user.id)
    print("continue")
    #files(user)
    debt.delay(user.id)  #
    history.delay(user.id)
    mark.delay(user.id)  #
    elective.delay(user.id)
    #message(user)  #
    print("Всего", time.time() - x)


# from push_notifications.models import GCMDevice

# device = GCMDevice.objects.get(user_id=13)
# The first argument will be sent as "message" to the intent extras Bundle
# Retrieve it with intent.getExtras().getString("message")
# device.send_message(title="Notification", message="You've got mail")

# device.send_message(None, badge=5)  # No alerts but with badge.
# device.send_message(message=None, extra={"foo": "bar"})  # Silent message with custom data.
# idinfo = 0
# upload = "https://lk.sut.ru/cabinet/project/cabinet/forms/message_create_stud.php"
# cookies = {'cookie': 'set', 'miden': '93ffc8717c3d7a03da19436d3554b2a9', 'uid': 'db0c22695811a717b4bc128a62473b3f'}
# data = {
#     "id": idinfo,
#     "upload": "",
#     "userfile": "image.png"
# }
#
# r = requests.post(upload, cookies=cookies, data=data, files={"userfile": open('image.png', 'rb')})
# for i in r.content.decode("windows-1251")[30:-9].split(";"):
#     if "data.idinfo" in i:
#         idinfo = int(i.split("=")[1].strip()[1:-1])
# print([idinfo])

