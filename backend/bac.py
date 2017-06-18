import datetime

def calculateBAC(alcDrink, volDrink, water, currentBCA):
    alc = alcDrink * 0.78924 * volDrink / 100
    alcInBlood = (alc / water) * 100
    currentBCA += alcInBlood
    return currentBCA


weight = 73
waterPercent = {'male': 0.7, 'female': 0.6}
sex = 'male'
water = weight * waterPercent[sex]
currentBCA = 0.0
drinkingStart = datetime.datetime.now()
alcDrink = 0.051
volDrink = 500
if (currentBCA == 0.0):
     drinkingStart = datetime.datetime.now()
currentBCA = calculateBAC(alcDrink, volDrink, water, currentBCA)
print(currentBCA)
