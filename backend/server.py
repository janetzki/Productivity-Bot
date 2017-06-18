from alcohol import calculate_bac, alcohol_amount, set_profile, reduced_bac, alcoholic_drinks, alcohol_contents, profile
from datetime import datetime, timedelta
from caffeine import caffeine_contents, reduced_caffeine, caffeine_history, caffeine_amount
from flask import Flask, request, jsonify
import requests
from mock_history import caffeine_mock_history, alcohol_mock_history
app = Flask(__name__)

minutes_past = 1337
minutes_future = 300
last_caffeine_time = datetime.now() - timedelta(hours=24)
last_drink = datetime.now() - timedelta(hours=24)

def second_difference(current_time):
    global last_caffeine_time
    difference = (current_time - last_caffeine_time).total_seconds()
    last_caffeine_time = current_time
    return difference


def second_difference_alc(current_time):
    global last_drink
    difference = (current_time - last_drink).total_seconds()
    last_drink = current_time
    return difference


def last_valid_drink(query_time):
    global caffeine_history
    last_valid = {}
    last_valid["total_caffeine"] = 0.0
    last_valid["timestamp"] = query_time
    for entry in caffeine_history:
        diff = (query_time - entry["timestamp"]).total_seconds()
        if diff >= 0:
            last_valid = entry
        else:
            return last_valid
    return last_valid


def last_valid_alc_drink(query_time):
    global alcoholic_drinks
    last_valid = {}
    last_valid["total_alcohol"] = 0.0
    last_valid["timestamp"] = query_time
    for entry in alcoholic_drinks:
        diff = (query_time - entry["timestamp"]).total_seconds()
        if diff >= 0:
            last_valid = entry
        else:
            return last_valid
    return last_valid


@app.route("/", methods=['GET', 'POST'])
def input_drink():
    return ""

@app.route("/alcohol/setprofile", methods=['GET', 'POST'])
def set_profile():
    if request.json != None:
        set_profile(request.json)
    return ""


@app.route("/alcohol/add", methods=['GET', 'POST'])
def alcohol_add(mock_input=None):
    global alcohol_amount, last_drink
    if mock_input == None:
        req = request.json
    else:
        req = mock_input
    if req != None and "timestamp" in req:
        add_time = datetime.strptime(req["timestamp"], "%a, %d %b %Y %H:%M:%S %Z")
    else:
        add_time = datetime.now()
    difference = second_difference_alc(add_time)
    alcohol_amount = reduced_bac(alcohol_amount, difference)
    if req != None and "drink" in req:
        drink = req["drink"]
        drinkVol = 500.0
        if "serving" in req:
            drinkVol = float(req["serving"])
        alcohol_amount += alcohol_contents(drink, drinkVol, add_time)
    return ""


@app.route("/alcohol/chart")
def alcohol_chart():
    global minutes_past, minutes_future, alcoholic_drinks
    current_time = datetime.now()
    chart = []
    for minute in range(-minutes_past, minutes_future + 1):
        delta_t = current_time + timedelta(minutes=minute)
        last_valid = last_valid_alc_drink(delta_t)
        diff = (delta_t - last_valid["timestamp"]).total_seconds()
        chart.append([delta_t, reduced_bac(last_valid["total_alcohol"], diff)])
    return jsonify(results=chart)


@app.route("/alcohol/history")
def alcohol_history():
    global alcoholic_drinks
    return jsonify(results=alcoholic_drinks)


@app.route("/alcohol/mock_history")
def alcohol_add_mock_history():
    global alcoholic_drinks, alcohol_mock_history, alcohol_add
    for history_object in alcohol_mock_history["results"]:
        alcohol_add(history_object)
    return ""


@app.route("/alcohol/profile")
def alcohol_profile():
    global profile
    return jsonify(results=profile)


@app.route("/caffeine/add", methods=['GET', 'POST'])
def caffeine_add(mock_input=None):
    global caffeine_amount, last_caffeine_time, caffeine_history
    if mock_input == None:
        req = request.json
    else:
        req = mock_input
    if req != None and "timestamp" in req:
        add_time = datetime.strptime(req["timestamp"], "%a, %d %b %Y %H:%M:%S %Z")
    else:
        add_time = datetime.now()
    difference = second_difference(add_time)
    caffeine_amount = reduced_caffeine(caffeine_amount, difference)
    if req != None and "drink" in req:
        drink = req["drink"]
        if "serving" in req:
            serving = req["serving"]
            caffeine_amount += caffeine_contents(drink, add_time, float(serving))
        else:
            caffeine_amount += caffeine_contents(drink, add_time)
    return ""


@app.route("/caffeine/history")
def caffeine_add_history():
    global caffeine_history
    return jsonify(results=caffeine_history)


@app.route("/caffeine/mock_history")
def caffeine_add_mock_history():
    global caffeine_history, caffeine_mock_history, caffeine_add
    for history_object in caffeine_mock_history["results"]:
        caffeine_add(history_object)
    return ""


@app.route("/caffeine/chart")
def caffeine_chart():
    global minutes_past, minutes_future, reduced_caffeine, caffeine_history
    current_time = datetime.now()
    chart = []
    for minute in range(-minutes_past, minutes_future + 1):
        delta_t = current_time + timedelta(minutes=minute)
        last_valid = last_valid_drink(delta_t)
        diff = (delta_t - last_valid["timestamp"]).total_seconds()
        chart.append([delta_t, reduced_caffeine(last_valid["total_caffeine"], diff)])
    return jsonify(results=chart)


app.run(debug=True)
