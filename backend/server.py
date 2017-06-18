from alcohol import calculate_bac, alcohol_amount, set_profile, reduced_bac, alcoholic_drinks, alcohol_contents
from datetime import datetime, timedelta
from caffeine import caffeine_contents, reduced_caffeine, caffeine_history, caffeine_amount
from flask import Flask, request, jsonify
app = Flask(__name__)

minutes = 360
last_caffeine_time = datetime.now()
last_drink = datetime.now()

@app.route("/alcohol/setprofile", methods=['GET', 'POST'])
def set_profile():
    if request.json != None:
        set_profile(request.json)
    return ""


@app.route("/alcohol/add", methods=['GET', 'POST'])
def alcohol_add():
    global alcohol_amount, last_drink
    difference = second_difference_alc(datetime.now())
    alcohol_amount = reduced_bac(alcohol_amount, difference)
    if request.json != None and "drink" in request.json:
        drink = request.json["drink"]
        drinkVol = 500.0
        if "serving" in request.json:
            drinkVol = float(request.json["serving"])
        alcohol_amount += alcohol_contents(drink, drinkVol)
    return ""


@app.route("/alcohol/chart")
def alcohol_chart():
    global minutes, alcoholic_drinks
    current_time = datetime.now()
    chart = []
    for minute in range(-minutes, minutes + 1):
        delta_t = current_time + timedelta(minutes=minute)
        last_valid = last_valid_alc_drink(delta_t)
        diff = (delta_t - last_valid["timestamp"]).total_seconds()
        chart.append([delta_t, reduced_bac(last_valid["total_alcohol"], diff)])
    return jsonify(results=chart)


@app.route("/alcohol/history")
def alcohol_history():
    global alcoholic_drinks
    return jsonify(results=alcoholic_drinks)


@app.route("/alcohol/profile")
def alcohol_profile():
    global profile
    return jsonify(results=profile)


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


@app.route("/caffeine/add", methods=['GET', 'POST'])
def caffeine_add():
    global caffeine_amount, last_caffeine_time
    difference = second_difference(datetime.now())
    caffeine_amount = reduced_caffeine(caffeine_amount, difference)
    if request.json != None and "drink" in request.json:
        drink = request.json["drink"]
        if "serving" in request.json:
            serving = request.json["serving"]
            caffeine_amount += caffeine_contents(drink, float(serving))
        else:
            caffeine_amount += caffeine_contents(drink)
    return ""


@app.route("/caffeine/history")
def caffeine_add_history():
    global caffeine_history
    return jsonify(results=caffeine_history)


@app.route("/caffeine/chart")
def caffeine_chart():
    global minutes, reduced_caffeine, caffeine_history
    current_time = datetime.now()
    chart = []
    for minute in range(-minutes, minutes + 1):
        delta_t = current_time + timedelta(minutes=minute)
        last_valid = last_valid_drink(delta_t)
        diff = (delta_t - last_valid["timestamp"]).total_seconds()
        chart.append([delta_t, reduced_caffeine(last_valid["total_caffeine"], diff)])
    return jsonify(results=chart)

app.run(debug=True)
