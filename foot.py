import telebot
from telebot import types
import random

TOKEN = "8621243334:AAFyWLkif15u6ZfxL5SkvsqIru7DCDq1Wek"
bot = telebot.TeleBot(TOKEN)

players = [
{"name":"Кріштіану Роналду","country":"Португалія","club":"Аль-Наср","pos":"Нападник"},
{"name":"Ліонель Мессі","country":"Аргентина","club":"Інтер Маямі","pos":"Нападник"},
{"name":"Кіліан Мбаппе","country":"Франція","club":"Реал Мадрид","pos":"Нападник"},
{"name":"Неймар","country":"Бразилія","club":"Аль-Хіляль","pos":"Нападник"},
{"name":"Ерлінг Голанд","country":"Норвегія","club":"Манчестер Сіті","pos":"Нападник"},
{"name":"Кевін Де Брюйне","country":"Бельгія","club":"Манчестер Сіті","pos":"Півзахисник"},
{"name":"Мохамед Салах","country":"Єгипет","club":"Ліверпуль","pos":"Нападник"},
{"name":"Роберт Левандовський","country":"Польща","club":"Барселона","pos":"Нападник"},
{"name":"Лука Модрич","country":"Хорватія","club":"Реал Мадрид","pos":"Півзахисник"},
{"name":"Гаррі Кейн","country":"Англія","club":"Баварія","pos":"Нападник"},
{"name":"Вінісіус Жуніор","country":"Бразилія","club":"Реал Мадрид","pos":"Нападник"},
{"name":"Джуд Беллінгем","country":"Англія","club":"Реал Мадрид","pos":"Півзахисник"},
{"name":"Букайо Сака","country":"Англія","club":"Арсенал","pos":"Півзахисник"},
{"name":"Родрі","country":"Іспанія","club":"Манчестер Сіті","pos":"Півзахисник"},
{"name":"Златан Ібрагімович","country":"Швеція","club":"Мілан","pos":"Нападник"},
{"name":"Сон Хин Мін","country":"Південна Корея","club":"Тоттенгем","pos":"Нападник"},
{"name":"Філ Фоден","country":"Англія","club":"Манчестер Сіті","pos":"Півзахисник"},
{"name":"Андрій Шевченко","country":"Україна","club":"Мілан","pos":"Нападник"},
{"name":"Олександр Зінченко","country":"Україна","club":"Арсенал","pos":"Захисник"},
{"name":"Михайло Мудрик","country":"Україна","club":"Челсі","pos":"Півзахисник"},
{"name":"Артем Довбик","country":"Україна","club":"Жирона","pos":"Нападник"},
{"name":"Ілля Забарний","country":"Україна","club":"Борнмут","pos":"Захисник"},
{"name":"Руслан Маліновський","country":"Україна","club":"Дженоа","pos":"Півзахисник"},
{"name":"Віктор Циганков","country":"Україна","club":"Жирона","pos":"Півзахисник"},
{"name":"Анатолій Трубін","country":"Україна","club":"Бенфіка","pos":"Воротар"},
{"name":"Андрій Лунін","country":"Україна","club":"Реал Мадрид","pos":"Воротар"}
]

countries=list(set([p["country"] for p in players]))
clubs=list(set([p["club"] for p in players]))
positions=["Нападник","Півзахисник","Захисник","Воротар"]

game_data={}

def main_menu(chat):
    kb=types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("Рандом 🪃","Гра 🕹️")
    bot.send_message(chat,"⚽ Головне меню",reply_markup=kb)

def send_random_player(chat):

    player=random.choice(players)

    text=f"""
⚽ Футболіст: {player['name']}

🌍 Країна: {player['country']}

🏟 Клуб: {player['club']}

🎯 Позиція: {player['pos']}
"""

    markup=types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Перевибрати ◀️",callback_data="reroll"))

    bot.send_message(chat,text,reply_markup=markup)

@bot.message_handler(commands=['start'])
def start(message):
    main_menu(message.chat.id)

@bot.message_handler(func=lambda m:m.text=="Рандом 🪃")
def random_mode(message):
    send_random_player(message.chat.id)

@bot.callback_query_handler(func=lambda call:call.data=="reroll")
def reroll(call):
    bot.delete_message(call.message.chat.id,call.message.message_id)
    send_random_player(call.message.chat.id)

@bot.message_handler(func=lambda m:m.text=="Гра 🕹️")
def game_start(message):

    player=random.choice(players)

    game_data[message.chat.id]={
        "player":player,
        "step":"remember",
        "mistakes":0
    }

    markup=types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Запам'ятав 🧠",callback_data="remember"))

    bot.send_message(message.chat.id,f"🧠 Запам'ятай футболіста\n\n⚽ {player['name']}",reply_markup=markup)

@bot.callback_query_handler(func=lambda c:c.data=="remember")
def start_questions(call):

    game_data[call.message.chat.id]["step"]="country"
    ask_country(call.message.chat.id)

def ask_country(chat):

    correct=game_data[chat]["player"]["country"]
    options=random.sample(countries,3)

    if correct not in options:
        options.append(correct)

    random.shuffle(options)

    kb=types.ReplyKeyboardMarkup(resize_keyboard=True)

    for o in options:
        kb.add(o)

    bot.send_message(chat,"🌍 Яка країна цього футболіста?",reply_markup=kb)

@bot.message_handler(func=lambda m:m.chat.id in game_data)
def game_logic(message):

    data=game_data[message.chat.id]
    player=data["player"]

    if data["mistakes"]>=10:
        bot.send_message(message.chat.id,"💀 10 помилок! Гру завершено.")
        del game_data[message.chat.id]
        main_menu(message.chat.id)
        return

    if data["step"]=="country":

        if message.text==player["country"]:
            data["step"]="club"
            ask_club(message.chat.id)
        else:
            data["mistakes"]+=1
            bot.send_message(message.chat.id,f"❌ Помилка ({data['mistakes']}/10)")

    elif data["step"]=="club":

        if message.text==player["club"]:
            data["step"]="pos"
            ask_pos(message.chat.id)
        else:
            data["mistakes"]+=1
            bot.send_message(message.chat.id,f"❌ Помилка ({data['mistakes']}/10)")

    elif data["step"]=="pos":

        if message.text==player["pos"]:
            data["step"]="name"
            ask_name(message.chat.id)
        else:
            data["mistakes"]+=1
            bot.send_message(message.chat.id,f"❌ Помилка ({data['mistakes']}/10)")

    elif data["step"]=="name":

        if message.text==player["name"]:
            bot.send_message(message.chat.id,"🏆 Правильно! Ти виграв!")
        else:
            bot.send_message(message.chat.id,f"❌ Ні! Це був {player['name']}")

        del game_data[message.chat.id]
        main_menu(message.chat.id)

def ask_club(chat):

    correct=game_data[chat]["player"]["club"]
    options=random.sample(clubs,3)

    if correct not in options:
        options.append(correct)

    random.shuffle(options)

    kb=types.ReplyKeyboardMarkup(resize_keyboard=True)

    for o in options:
        kb.add(o)

    bot.send_message(chat,"🏟 В якому клубі він грає?",reply_markup=kb)

def ask_pos(chat):

    correct=game_data[chat]["player"]["pos"]
    options=random.sample(positions,3)

    if correct not in options:
        options.append(correct)

    random.shuffle(options)

    kb=types.ReplyKeyboardMarkup(resize_keyboard=True)

    for o in options:
        kb.add(o)

    bot.send_message(chat,"🎯 Яка його позиція?",reply_markup=kb)

def ask_name(chat):

    names=[p["name"] for p in players]
    player=game_data[chat]["player"]

    options=random.sample(names,4)

    if player["name"] not in options:
        options.append(player["name"])

    random.shuffle(options)

    kb=types.ReplyKeyboardMarkup(resize_keyboard=True)

    for o in options:
        kb.add(o)

    bot.send_message(chat,"👤 Хто це був?",reply_markup=kb)

bot.infinity_polling()