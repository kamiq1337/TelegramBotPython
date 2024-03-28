import telebot,random 
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup 
from info import description, history, date
from telegram.ext import Updater, CommandHandler, MessageHandler, filters

bot = telebot.TeleBot('YOU_TOKEN')
@bot.message_handler(commands=['start']) 
def start_bot(message): 
    bot.send_message(chat_id=message.chat.id, text='я - бот написанный на Python. Я могу рассказать Вам о различных настольных играх, а так же сыграть с Вами в небольшую игру! Для того чтобы воспользоваться моими функциями используйте команду /help')
@bot.message_handler(commands=['help']) 
def start_bot(message): 
    keyboard = InlineKeyboardMarkup() 
    keyboard.add(InlineKeyboardButton("Топ 10 игр", callback_data='description'),
                 InlineKeyboardButton("Игра", callback_data='game') ) 
    keyboard.add(InlineKeyboardButton("История создания", callback_data='history'), 
                 InlineKeyboardButton("Дата создания", callback_data='date'), ) 
    bot.send_message(chat_id=message.chat.id, text='Чем я могу Вам помочь?', reply_markup=keyboard) 
@bot.message_handler(content_types=['text'])
def echo(message):
    if message.text.__contains__('привет') or message.text.__contains__('Привет'):
        bot.send_message(message.chat.id, 'привет!))')
    elif message.text.__contains__('пока'):
        bot.send_message(message.chat.id, 'покеда!')
@bot.callback_query_handler(func=lambda call: True) 
def query_handler(call): 
    if call.data == 'description': 
        description_info = ', '.join(description.keys())
        bot.send_message(chat_id=call.message.chat.id, text="О какой игре вы хотите узнать? " + description_info +'.') 
        bot.register_next_step_handler(call.message, print_info_description)
    elif call.data == 'history': 
        history_info = ', '.join(history.keys()) 
        bot.send_message(chat_id=call.message.chat.id, text="Игры, историю создания которых я могу рассказать: " + history_info +'. Выбери тему.')
        bot.register_next_step_handler(call.message, print_info_history)
    elif call.data == 'date': 
        date_info = ', '.join(date.keys())
        bot.send_message(chat_id=call.message.chat.id, text="Я могу рассказать вам о датах создания таких игр: " + date_info +'. Выберите интересующую Вас игру') 
        bot.register_next_step_handler(call.message, print_info_date)
    elif call.data=='game':
       bot.send_message(chat_id=call.message.chat.id, text="Чтобы запустить игру используйте команду /game")

def print_info_description(message): 
    if message.text in description: 
        bot.send_message(chat_id=message.chat.id, text=description[message.text]) 
    else: 
        bot.send_message(chat_id=message.chat.id, text='Я не знаю эту игру') 
    start_bot(message)
def print_info_history(message): 
    if message.text in history: 
        bot.send_message(chat_id=message.chat.id, text=history[message.text]) 
    else: 
        bot.send_message(chat_id=message.chat.id, text='Я не знаю историю создания этой игры') 
    start_bot(message)
def print_info_date(message): 
    if message.text in date: 
        bot.send_message(chat_id=message.chat.id, text=date[message.text]) 
    else: 
        bot.send_message(chat_id=message.chat.id, text='Я не знаю дату создания этой игры') 
    start_bot(message)
@bot.message_handler(func=lambda message: message.text.lower() == "game")
def digitgames(message):
    init_storage(message.chat.id)
    attempt = 10
    set_data_storage(message.chat.id, "attempt", attempt)

    bot.send_message(message.chat.id, f'Игра "угадай число"!\nКоличество попыток: {attempt}')

    random_digit = random.randint(1, 10)
    set_data_storage(message.chat.id, "random_digit", random_digit)

    bot.send_message(message.chat.id, 'Готово! Загадано число от 1 до 10!')
    bot.send_message(message.chat.id, 'Введите число')
    bot.register_next_step_handler(message, process_digit_step)

def process_digit_step(message):
    user_digit = message.text

    if not user_digit.isdigit() or int(user_digit) < 1 or int(user_digit) > 10:
        msg = bot.reply_to(message, 'Вы ввели некорректное число. Введите число от 1 до 10')
        bot.register_next_step_handler(msg, process_digit_step)
        return

    attempt = get_data_storage(message.chat.id)["attempt"]
    random_digit = get_data_storage(message.chat.id)["random_digit"]

    if int(user_digit) == random_digit:
        bot.send_message(message.chat.id, f'Ура! Ты угадал число! Это была цифра: {random_digit}')
        init_storage(message.chat.id)
        return

    elif attempt > 1:
        attempt -= 1
        set_data_storage(message.chat.id, "attempt", attempt)
        bot.send_message(message.chat.id, f'Неверно, осталось попыток: {attempt}')
        bot.register_next_step_handler(message, process_digit_step)
    else:
        bot.send_message(message.chat.id, 'Вы проиграли!')
        init_storage(message.chat.id)
        return

if __name__ == '__main__':
    bot.polling()