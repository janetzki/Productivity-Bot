from datetime import datetime, timedelta
from caffeine import caffeine_contents, reduced_caffeine, caffeine_history, caffeine_amount
from flask import Flask, request, jsonify
app = Flask(__name__)
server_caffeine_amount = 0.0
last_caffeine_time = datetime.now()
minutes = 360

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

@app.route("/caffeine/add")
def caffeine_add():
	global caffeine_amount, last_caffeine_time, server_caffeine_amount
	difference = second_difference(datetime.now())
	caffeine_amount = reduced_caffeine(caffeine_amount, difference)
	server_caffeine_amount = caffeine_amount
	if "drink" in request.form:
		drink = request.form["drink"]
		if "serving" in request.form:
			serving = request.form["serving"]
			caffeine_amount += caffeine_contents(drink, float(serving))
		else:
			caffeine_amount += caffeine_contents(drink)
	else:
		caffeine_amount += caffeine_contents('mate')
	return ""

@app.route("/caffeine/add/history")
def caffeine_add_history():
	global caffeine_history
	return jsonify(results = caffeine_history)

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
	return jsonify(results = chart)

app.run(debug=True)
