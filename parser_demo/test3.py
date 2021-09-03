import re
import requests
import datetime
from bs4 import BeautifulSoup
from sqler import sql_insert_many_dict, sql_insert_dict, save_changes, tutor_copy

start = datetime.datetime(2020, 9, 1)
counter = 0


def request(date='', type_z='', fac='', number='', credit=False):
    global counter
    print(counter)
    url = "https://cabinet.sut.ru/raspisanie_all_new"
    counter += 1
    data_ = {
        "schet": date,
        "type_z": type_z,
        "faculty": fac,
        "group": number
    }
    if credit: data_["rasp_zach"] = True
    resp = requests.session()
    resp = resp.post(url=url, data=data_)
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


semester_date = []
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

groups = []
for i, j in faculty.items():
    for k, l in j["groups"].items():
        groups.append({i: l})
print(faculty)
print(groups)
sql_insert_many_dict("timetable_group", ["faculty", "group"], groups)
save_changes()
data = {}

counter = 0
for fac_name, fac_items in faculty.items():
    for group_id, group_name in fac_items["groups"].items():

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
                        data["date"] = time_corrector(k, w)

                        if tutor_full_tmp:
                            for num, name in enumerate(tutor_tmp):
                                data["tutor_full"] = tutor_full_tmp[num]
                                if name.isupper():  # Костыль для записи АЛЕКСЕЕВА О.М
                                    temp = name.split()
                                    name = "{0} {1}".format(temp[0].capitalize(), temp[1])
                                # Костыль для записи Киселева А.В
                                name = "Киселёва А.В" if name == "Киселева А.В" else name
                                data["tutor"] = name
                                sql_insert_dict("timetable_timetable", data)
                                print(data)
                        else:
                            sql_insert_dict("timetable_timetable", data)
                            print(data)
        data.clear()

        # Зачеты
        j = request(semester_date[0], "1", fac_items["id"], group_id, True).find("tbody")
        if j:
            data["group"] = group_name
            data["faculty"] = fac_name
            for i in j.find_all("tr")[1:]:
                k = i.find_all("td")
                data["date"] = datetime.datetime.strptime(re.sub(r"[а-яА-Я a-zA-Z]", "", k[0].text), "%d.%m.%Y")
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
                        sql_insert_dict("timetable_timetable", data)
                        print(data)
                else:
                    sql_insert_dict("timetable_timetable", data)
                    print(data)
        data.clear()

        # Экзамены
        # for i in request(semester_date[0], "2", fac_items["id"], group_id).find("table").find_all("tr")[1:-1]:
        #     pass

save_changes()
tutor_copy()
save_changes()
# sql_insert_dict("timetable_timetable", data)

