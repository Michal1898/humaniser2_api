from flask import Flask, jsonify, request

import csv
import datetime
import random
from random import choice, randrange, getrandbits
from datetime import timedelta, date
from random import shuffle
from dateutil.relativedelta import relativedelta
import os
from radar import random_datetime

FEMALE = True
MALE = False

app = Flask(__name__)

@app.route("/")
def dummy_api():
    person = {}
    age_max=99
    age_min=1
    gender=MALE

    count=int(request.args.get("count"))
    gender2=str(request.args.get("sex"))
    gender2=gender2.upper()
    if gender2=="FEMALE":
        gender=FEMALE

    current_date = date.today()
    start_date = current_date - relativedelta(years=age_max)
    end_date = current_date - relativedelta(years=age_min)


    humaniser_py_path = os.path.dirname(os.path.realpath(__file__))

    if gender == FEMALE:
        first_names_file = os.path.join(humaniser_py_path, "names_cr", "krestni_zeny.csv")
        surnames_file = os.path.join(humaniser_py_path, "names_cr", "prijmeni_zeny_1.csv")

    else:
        first_names_file = os.path.join(humaniser_py_path, "names_cr", "krestni_muzi.csv")
        surnames_file = os.path.join(humaniser_py_path, "names_cr", "prijmeni_muzi_1.csv")

    with open(first_names_file, encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        data = list(reader)

    first_names_list = data[:150]

    with open(surnames_file, encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        data = list(reader)

    surnames_list = data[:150]

    addresses = []
    address_folder = os.path.join(humaniser_py_path, "addresses_cr")
    for adr_index in range(1, 8):
        addr_file_name = "adr_" + str(adr_index) + ".csv"
        addr_file = os.path.join(address_folder, addr_file_name)
        with open(addr_file, encoding="utf-8", newline="") as f:
            reader = csv.reader(f)
            data = list(reader)
            addresses.extend(data[1:])

    human_list = []
    for c in range(0, count):
        person = {}
        person["gender"] = gender

        random_first_name = choice(first_names_list)
        person["firstname"] = random_first_name[1]

        random_surname = choice(surnames_list)
        person["surname"] = random_surname[1]

        random_date = random_datetime(
            start=start_date,
            stop=end_date
        )
        person["birthdate"] = random_date

        random_address = choice(addresses)
        random_address = random_address[0]
        random_address = random_address.split(";", -1)

        person["city"] = random_address[0]
        person["street"] = random_address[1]
        person["house_no"] = random_address[2]
        person["plz"] = random_address[3]

        # print (person)
        human_list.append(person)

    return jsonify(human_list)


if __name__ == "__main__":
    app.run()