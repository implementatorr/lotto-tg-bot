from telebot import types
import random

bot = telebot.TeleBot("your token")

buttons = [types.InlineKeyboardButton(str(i), callback_data=str(i)) for i in range(1, 26)]
keyboard = types.InlineKeyboardMarkup(row_width=5)
keyboard.add(*buttons)

user_result = []

winning_numbers = []


def number_to_string(number):
    return str(number)


def check_matches(chat_id, user_result, winning_numbers):
    matches = []
    user_result = list(user_result)
    winning_numbers = list(winning_numbers)

    for i in user_result:
        for k in winning_numbers:
            if int(i) == int(k):
                matches.append(i)
    if len(matches) == 6:
        matches_str = ", ".join(map(str, matches))
        bot.send_message(chat_id, f"Поздравляем! Вы угадали все числа: {matches_str}. Вы выиграли подписку на год!")
    elif len(matches) == 5:
        matches_str = ", ".join(map(str, matches))
        bot.send_message(chat_id, f"Поздравляем! Вы угадали 5 чисел: {matches_str}. Вы выиграли подписку на месяц!")
    elif len(matches) >= 1:
        matches_str = ", ".join(map(str, matches))
        bot.send_message(chat_id, f"Поздравляем! Вы угадали числа: {matches_str}. У вас есть шанс выиграть еще больше!")
    else:
        bot.send_message(chat_id, "Увы, у вас нет совпадений. Попробуйте еще раз!")


@bot.message_handler(commands=["start"])
def start(message):
    global user_result, winning_numbers
    rules = (
        "Добро пожаловать в лотерею! 🌟\n\n"
        "Правила участия:\n"
        "1. Выберите 6 чисел от 0 до 25.\n"
        "2. Мы случайным образом выберем 6 выигрышных чисел.\n"
        "3. Если вы угадываете 5 чисел, вы получаете подписку на месяц в *Telegram Premium* 🥇\n"
        "4. Если угадываете все 6 чисел, вы выигрываете подписку *Telegram Premium* на *год*! 🎉"
    )
    user_result = []
    winning_numbers = []
    bot.send_message(message.chat.id, rules, reply_markup=keyboard, parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: True)
def handle_button_click(call):
    global user_result
    user_result.sort()
    selected_value = call.data

    if selected_value not in user_result:
        user_result.append(selected_value)
        remaining_numbers = 6 - len(user_result)
        bot.answer_callback_query(call.id,
                                  text=f"Вы выбрали число {number_to_string(selected_value)}. Осталось выбрать: {remaining_numbers} чисел.")

    if len(user_result) == 6:
        user_result.sort()
        result_string = [number_to_string(number) for number in user_result]

        if " | ".join(result_string) != call.message.text:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f"Вы выбрали числа: {', '.join(result_string)}. Осталось выбрать: 0 чисел.")

        bot.send_message(call.message.chat.id, "🎁🎁🎁 Идет розыгрыш лотереи 🎁🎁🎁",
                         reply_markup=types.ReplyKeyboardRemove())

        result, winning_numbers = lotto(user_result)
        bot.send_message(call.message.chat.id,
                         f"Выигрышные числа: {', '.join(number_to_string(num) for num in winning_numbers)}")

        check_matches(call.message.chat.id, user_result, winning_numbers)


def lotto(nums: list):
    random_numbers = random.sample(range(1, 25), 6)
    index = 0
    result = []
    for rando in random_numbers:
        for num in nums:
            if rando == num:
                index += 1
                result.append(rando)
                if index == 6:
                    return result, random_numbers
    return result.sort(), random_numbers


bot.polling()

