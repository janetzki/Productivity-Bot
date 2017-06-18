from alcohol import calculate_bac, alcohol_amount, set_profile, reduced_bac, alcoholic_drinks, alcohol_contents, profile
from datetime import datetime, timedelta
from caffeine import caffeine_contents, reduced_caffeine, caffeine_history, caffeine_amount, time_till_nth
from flask import Flask, request, jsonify
from mock_history import caffeine_mock_history, alcohol_mock_history
import time
from operator import itemgetter
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
    for entry in sorted(caffeine_history, key=lambda hist: hist["timestamp"]):
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
    for entry in sorted(alcoholic_drinks, key=lambda hist: hist["timestamp"])::
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

@app.route("/alcohol/recommendation")
def alcohol_recommendation():
    global alcohol_amount
    lower = 1.29
    upper = 1.38
    current_time = datetime.now()
    current_alcohol = reduced_bac(alcohol_amount, second_difference_alc(current_time))
    response = ""
    if current_alcohol == 0.0:
        response += "You should better start drinking if you wanna hit the balmer peak and be more productive"
        if int(current_time.strftime('%H')) < 16:
            response += ". Maybe it is a bit early but hey it is your liver."
    elif current_alcohol + calculate_bac() < lower:
        if current_alcohol + calculate_bac() > upper:
            minutes = (upper - current_alcohol - calculate_bac())/-0.15*60
            response += "You are one beer away from hitting the ballmer peak if you start drinking in %d minutes you will get the most benefits." % int(minutes)
        else:
            count = (lower - current_alcohol)/calculate_bac()
            if count <= 1:
                minutes = ((upper - current_alcohol - calculate_bac())/-0.15)*60
                response += "You are almost there. Drink your next beer in %d minutes to get in the zone." % int(minutes)
            elif count < 2:
                response += "You are about 1 beer away from hitting the ballmer peak to be most productive."
            else:
                response += "You are %d beers away from hitting the ballmer peak to be most productive." % int(count)
    elif current_alcohol < upper and current_alcohol > lower:
        minutes = (upper - current_alcohol - calculate_bac())/-0.15*60
        response += "You are in the ballmer peak you should be most productive right know so start being productive drink your next beer in %d minutes to stay in the zone." % int(minutes)
    elif current_alcohol > upper:
        minutes = (upper - current_alcohol)/-0.15*60
        response += "Well you already ahead of the ballmer peak you can wait %d minutes and enter the ballmer peak or start partying." % int(minutes)
    return jsonify(results=response)

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


@app.route("/caffeine/recommendation")
def caffeine_recommendation():
    global caffeine_amount
    lower_thresh = 100.0
    upper_thresh = 250.0
    current_caffeine = reduced_caffeine(caffeine_amount, second_difference(datetime.now()))
    response = ""
    if caffeine_amount < 1.0:
        response = "You better start drinking mate. You need at least one mate to reach the sweet spot."
    elif caffeine_amount < lower_thresh:
        needed_max = (upper_thresh - caffeine_amount) / 100.0
        if 100.0 * int(needed_max) >= lower_thresh:
            needed_mate = int(needed_max)
        else:
            needed_mate = int(needed_max) + 1
        response = "You need to drink up to %d more mate to reach the sweet spot." % needed_mate
    elif caffeine_amount < upper_thresh:
        response = "You did it! Start being productive."
    else:
        nth_particles = int(caffeine_amount / lower_thresh)
        needed_time = int(time_till_nth(nth_particles) / 60.0)
        response = "Are you trembling yet? You should wait at least %d minutes until you drink a mate again." % needed_time
    return jsonify(results=response)

app.run(debug=True)
