from alcohol import calculateBAC
from datetime import datetime, timedelta
from caffeine import caffeine_contents, reduced_caffeine, caffeine_history, caffeine_amount
from flask import Flask, request, jsonify
app = Flask(__name__)

minutes = 360
last_caffeine_time = datetime.now()
lastDrink = datetime.now()

server_caffeine_amount = 0.0
waterPercent = {'male': 0.7, 'female': 0.6 }

currentBCA = 0.35

profile = {}
profile["age"] = "18"
profile["sex"] = "male"
profile["weight"] = "65.0"
alcoholicDrinks = []

def water():
    return float(profile["weight"]) * float(waterPercent[profile["sex"]])

@app.route("/alcohol/setprofile", methods=['GET', 'POST'])
def set_profile():
    global profile
    profile["age"] = request.json["age"]
    profile["sex"] = request.json["sex"]
    profile["weight"] = request.json["weight"]
    return ""

@app.route("/alcohol/add", methods=['GET', 'POST'])
def alcohol_add():
    if request.json != None and "drink" in request.json:
        drink = request.json["drink"]
        drinkVol = 500.0
        if "serving" in request.json:
            serving = request.json["serving"]
            drinkVol = float(serving)
        drinkTime = datetime.now()
        alcoholicDrinks.append((drink, drinkVol, drinkTime))
    return ""

@app.route("/alcohol/chart")
def alcohol_chart():
    global alcoholicDrinks, minutes

    currentBCA = 0.0
    if len(alcoholicDrinks) > 0:
        lastDrink = alcoholicDrinks[0][2]
    currentTime = datetime.now()
    data = [[currentTime + timedelta(minutes=i), 0] for i in range(-minutes, minutes)]
    print(alcoholicDrinks)
    for drink in alcoholicDrinks:
        time = drink[2]
        mins = int((time - lastDrink).total_seconds() / 60)
        # drinkAlc = drinkMap[drink[0]]
        drinkAlc = 0.05
        drinkVol = drink[1]
        diff = int((currentTime - lastDrink).total_seconds() / 60)
        for t in range(0, mins):
            currentBCA = currentBCA - 0.15 * (1 / 60)
            currentBCA = max(0, currentBCA)
            if diff-t <= minutes:
                data[minutes-(diff-t)] = [currentTime - timedelta(minutes=diff-t), currentBCA]
        currentBCA += calculateBAC(drinkAlc, drinkVol, water())
        if diff-mins <= minutes:
            data[minutes-(diff-mins)] = [currentTime - timedelta(minutes=diff-mins), currentBCA]
    for t in range(minutes, 2*minutes):
        currentBCA = currentBCA - 0.15 * (1 / 60)
        currentBCA = max(0, currentBCA)
        data[t] = [currentTime + timedelta(minutes=t-minutes), currentBCA]
    return jsonify(results = data)

@app.route("/alcohol/history")
def alcohol_history():
    global alcoholicDrinks
    return jsonify(results=alcoholicDrinks)

@app.route("/alcohol/profile")
def alcohol_profile():
    global profile
    return jsonify(results=profile)

def second_difference(current_time):
    global last_caffeine_time
    difference = (current_time - last_caffeine_time).total_seconds()
    last_caffeine_time = current_time
    return difference

def last_valid_drink(query_time):
    global last_caffeine_time, caffeine_history
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

@app.route("/caffeine/add", methods=['GET', 'POST'])
def caffeine_add():
    global caffeine_amount, last_caffeine_time, server_caffeine_amount
    difference = second_difference(datetime.now())
    caffeine_amount = reduced_caffeine(caffeine_amount, difference)
    server_caffeine_amount = caffeine_amount
    if request.json != None and "drink" in request.json:
        drink = request.json["drink"]
        if "serving" in request.json:
            serving = request.json["serving"]
            caffeine_amount += caffeine_contents(drink, float(serving))
        else:
            caffeine_amount += caffeine_contents(drink)
    return ""


@app.route("/caffeine/add/history")
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
