from alcohol import calculateBAC
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
app = Flask(__name__)

weight = 65
waterPercent = {'male': 0.7, 'female': 0.6}
sex = 'male'
water = weight * waterPercent[sex]
currentBCA = 0.35
lastDrink = datetime.now()
minutes = 360

alcoholicDrinks = []


@app.route("/alcohol/add")
def alcohol_add():
    # drink = request.form['drink']
    drink = "Bier"
    drinkVol = 500.0
    drinkTime = datetime.now()
    alcoholicDrinks.append((drink, drinkVol, drinkTime))
    return ""

@app.route("/alcohol/chart")
def alcohol_chart():
    global alcoholicDrinks, water, minutes

    currentBCA = 0.0
    if len(alcoholicDrinks) > 0:
        lastDrink = alcoholicDrinks[0][2]
    currentTime = datetime.now()
    data = [[0,currentTime + timedelta(minutes=i)] for i in range(-minutes, minutes)]
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
            if currentBCA <= 0:
                currentBCA = 0
            if diff-t <= minutes:
                data[minutes-(diff-t)] = [currentBCA, currentTime - timedelta(minutes=diff-t)]
        currentBCA += calculateBAC(drinkAlc, drinkVol, water)
        if diff-mins <= minutes:
            data[minutes] = [currentBCA, currentTime]
    currentBCA = data[minutes][0]
    for t in range(minutes, 2*minutes):
        currentBCA = currentBCA - 0.15 * (1 / 60)
        if currentBCA <= 0:
            currentBCA = 0
        data[t] = [currentBCA, currentTime + timedelta(minutes=t-minutes)]
    return jsonify(results = data)

app.run(debug=True)
