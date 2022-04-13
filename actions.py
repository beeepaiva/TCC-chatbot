from datetime import date, timedelta, datetime

def convertNum(text):
    if text == "primeiro" or text == "um" or text == "hum" or text == "1" or text == "1º":
        return 1
    elif text == "segundo" or text == "dois"or text == "2" or text == "2º":
        return 2
    elif text == "terceiro" or text == "três" or text == "tres" or text == "3" or text == "3º":
        return 3
    elif text == "quarto" or text == "quatro" or text == "4" or text == "4º":
        return 4
    elif text == "quinto" or text == "cinco" or text == "5" or text == "5º":
        return 5
    elif text == "sexto" or text == "seis" or text == "6" or text == "6º":
        return 6
    elif text == "sétimo" or text == "setimo" or text == "sete" or text == "7" or text == "7º":
        return 7
    elif text == "oitavo" or text == "oito" or text == "8" or text == "8º":
        return 8
    else:
        return 0

def convertDate(text):
    if text == "hoje":
        return date.today()
    elif text == "amanhã" or text == "amanha" or text == "depois de hoje":
        return date.today()+ timedelta(days=1)
    elif text == "depois de amanhã" or text == "depois de amanha":
        return date.today()+ timedelta(days=2)
    elif text == "segunda" or text == "2ª":
        return nextDayOf(date.today(), 0)
    elif text == "terça" or text == "terca" or text == "3ª":
        return nextDayOf(date.today(), 1)
    elif text == "quarta" or text == "4ª":
        return nextDayOf(date.today(), 2)
    elif text == "quinta" or text == "5ª":
        return nextDayOf(date.today(), 3)
    elif text == "sexta" or text == "6ª":
        return nextDayOf(date.today(), 4)
    else:
        return 0

def nextDayOf(d, weekday):
    ahead = weekday - d.weekday()
    if ahead <= 0:
        ahead += 7
    return d + timedelta(ahead)