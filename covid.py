from covid19_data import JHU


def getcorona(country):
    final_message = ""
    get_message_bot = country
    if get_message_bot == "сша":
        final_message = "🇺🇸Данные по США: " + "\n🦠Заболевшие: " + str(JHU.US.confirmed) + "\n☠️Умершие: " + str(JHU.US.deaths) + "\n💊Выздоровевшие: " + str(JHU.US.recovered)

    elif get_message_bot == "россия":
        final_message = "🇷🇺Данные по России: " + "\n🦠Заболевшие: " + str(JHU.Russia.confirmed) + "\n☠️Умершие: " + str(JHU.Russia.deaths) + "\n💊Выздоровевшие: " + str(JHU.Russia.recovered)

    elif get_message_bot == "япония":
        final_message = "🇯🇵Данные по Японии: " + "\n🦠Заболевшие: " + str(JHU.Japan.confirmed) + "\n☠️Умершие: " + str(JHU.Japan.deaths) + "\n💊Выздоровевшие: " + str(JHU.Japan.recovered)
        
    elif get_message_bot == "италия":
        final_message = "🇮🇹Данные по Италии: " + "\n🦠Заболевшие: " + str(JHU.Italy.confirmed) + "\n☠️Умершие: " + str(JHU.Italy.deaths) + "\n💊Выздоровевшие: " + str(JHU.Italy.recovered)
    else:
        final_message = "🌍Данные по всему миру: " "\n🦠Заболевшие: " + str(JHU.Total.confirmed) + "\n☠️Умершие: " + str(JHU.Total.deaths) + "\n💊Выздоровевшие: " + str(JHU.Total.recovered)

    return final_message