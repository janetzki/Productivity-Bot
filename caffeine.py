import csv
import sys
import math

caffeine_half_time_sec = 14400
lambda_coeff = math.log(2) / caffeine_half_time_sec
caffeine_history = []

def reduced_caffeine(amount, time):
	return amount * math.exp(-lambda_coeff * time)

def caffeine_for_drink(drink):
	# source http://koffein.com/
	caffeine_dict = {}
	with open('caffeine_contents.csv', newline='\n') as csvfile:
		for row in csv.reader(csvfile, delimiter=',', quotechar='"'):
			caffeine_dict[row[0].lower()] = float(row[1])
	amount = caffeine_dict.get(drink)
	if amount != None:
		return float(amount)
	else:
		contains_matches = [value for key, value in caffeine_dict.items() if drink in key]
		if len(contains_matches) > 0:
			return max(contains_matches)
		else:
			return 0.0

def caffeine_contents(drink, serving_size = 500.0):
	caffeine_per_100 = caffeine_for_drink(drink)
	amount = caffeine_per_100 * serving_size / 100.0
	caffeine_history.add('"' + drink + '",' + serving_size + ',' + amount)
	return amount

if __name__ == "__main__":
	if len(sys.argv) > 1:
		drink = sys.argv[1].lower()
		if len(sys.argv) > 2:
			serving = float(sys.argv[2])
			caffeine = caffeine_contents(drink, serving)
		else:	
			caffeine = caffeine_contents(drink)
		print(caffeine)
	if len(sys.argv) > 3:
		time_delta = int(sys.argv[3])
		print(reduced_caffeine(caffeine, time_delta))
		