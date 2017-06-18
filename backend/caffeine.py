import csv
import math
from datetime import datetime

caffeine_half_time_sec = 14400
lambda_coeff = math.log(2) / caffeine_half_time_sec
caffeine_history = []
caffeine_amount = 0.0

def reduced_caffeine(amount, time):
    return amount * math.exp(-lambda_coeff * time)

def caffeine_for_drink(drink):
    # source http://koffein.com/
    caffeine_dict = {}
    with open('backend/caffeine_contents.csv', newline='\n') as csvfile:
        for row in csv.reader(csvfile, delimiter=',', quotechar='"'):
            caffeine_dict[row[0].lower()] = float(row[1])
    amount = caffeine_dict.get(drink)
    if amount is not None:
        return float(amount)
    else:
        contains_matches = [value for key, value in caffeine_dict.items() if drink in key]
        if len(contains_matches) > 0:
            return max(contains_matches)
        else:
            return 0.0


def caffeine_contents(drink, serving_size = 500.0):
    global caffeine_amount
    caffeine_per_100 = caffeine_for_drink(drink.lower())
    amount = caffeine_per_100 * serving_size / 100.0
    current_time = datetime.now()
    if len(caffeine_history) > 0:
        last_element = caffeine_history[-1]
        diff = (current_time - last_element["timestamp"]).total_seconds()
        caffeine_amount = reduced_caffeine(caffeine_amount, diff)
    caffeine_amount += amount
    history_object = {}
    history_object["drink"] = drink
    history_object["serving"] = serving_size
    history_object["caffeine"] = amount
    history_object["total_caffeine"] = caffeine_amount
    history_object["timestamp"] = current_time
    caffeine_history.append(history_object)
    return amount
