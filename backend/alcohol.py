import datetime

def calculateBAC(alcDrink, volDrink, water):
    alc = alcDrink * 0.78924 * volDrink / 100
    alcInBlood = (alc / water) * 100
    return alcInBlood
