import telebot
from tic_tac_toe import game
import log_generate as lg

bot = telebot.TeleBot('TOKEN')
chat_id = ''
dic = {}

@bot.message_handler(commands=['start'])
def start(message):
    lg.write_data(f'Бот получил команду "{message.text}"')
    bot.send_message(message.chat.id, f'Привет {message.from_user.first_name}!')
    bot.send_message(message.chat.id, 'Будем играть в крестики-нолики:\n'
                                      'поиграем\nпомощь')
    bot.send_message(message.chat.id, f'Поиграем')

@bot.message_handler(commands=['help'])
def help(message):
    lg.write_data(f'Бот получил команду "{message.text}"')
    bot.send_message(chat_id, 'Привет:\n'
                              '/start - команда приветствия\n'
                              'Игра в крестики-нолики;\n'
                              '/help - вывод слов;')

@bot.message_handler()
def get_user_text(message):  # Выбор функций бота
    lg.write_data(f'Бот получил команду "{message.text}"')
    mes = message
    global chat_id
    chat_id = mes.chat.id
    if mes.text.lower() == 'поиграем':
        bot.send_message(chat_id, 'У меня нолики! Ты ходи первым.')
        lg.write_data(f'Игра "крестики-нолики"')
        global dic
        dic = {'1': '.', '2': '.', '3': '.', '4': '.', '5': '.', '6': '.', '7': '.', '8': '.', '9': '.'}
        lg.write_data(f'Словарь заполнен точками')
        bot.register_next_step_handler(mes, start_game)
    else:
        lg.write_data(f'Зафиксирована неизвестная команда')
        bot.send_message(message.chat.id, 'Я тебя не понимаю! Воспользуйся командой "/help"!')

def start_game(message):  # Функция определения, кто будет ходить первым
    if message.text == 'да':
        lg.write_data(f'Пользователь принял решение ходить первым')
        bot.send_message(chat_id, 'Выбери клетку!')
        bot.register_next_step_handler(message, user_check)
    elif message.text == 'нет':
        lg.write_data(f'Бот ходит первым')
        bot.send_message(chat_id, 'Хорошо, я начинаю!')
        pc_check()
    else:
        lg.write_data(f'В функции определения хода зафиксирована неизвестная команда "{message.text}"')
        bot.send_message(chat_id, 'Я тебя не понял! Скажи еще раз!')
        bot.register_next_step_handler(message, start_game)

def user_check(message):  # Ход пользователя
    global dic
    lg.write_data(f'Начался ход пользователя')
    player_turn = message.text
    if player_turn in ('1', '2', '3', '4', '5', '6', '7', '8', '9') and dic.get(player_turn) == '.':
        dic[player_turn] = 'x'
        lg.write_data(f'Пользователь выбрал клетку: {player_turn}')
        if game.check_winner(dic):
            lg.write_data(f'Пользователь победил в игре')
            bot.send_message(chat_id, 'Ты выиграл!')
        elif '.' not in dic.values():
            lg.write_data(f'Игра завершилась ничьей')
            bot.send_message(chat_id, 'Ой у нас ничья!')
        else:
            bot.send_message(chat_id, game.print_dic(dic))
            pc_check()
    else:
        lg.write_data(f'На ходе пользователя зафиксирован не корректный ввод: {player_turn}')
        bot.send_message(chat_id, 'Ты что-то не то ввел! Попробуй еще раз!')
        bot.register_next_step_handler(message, user_check)

def pc_check():  # Ход бота
    global dic
    lg.write_data(f'Начался ход бота')
    bot.send_message(chat_id, 'Мой ход:')
    bot_choice = game.pc_choice(dic)
    lg.write_data(f'Бот выбирает клетку {bot_choice}')
    dic[bot_choice] = '0'
    bot.send_message(chat_id, game.print_dic(dic))
    if game.check_winner(dic):
        lg.write_data(f'Бот победил в игре')
        bot.send_message(chat_id, 'Я победил!')
    elif '.' not in dic.values():
        lg.write_data(f'Игра завершилась ничьей')
        bot.send_message(chat_id, 'Ой у нас ничья!')
    else:
        message = bot.send_message(chat_id, 'Твой ход!')
        bot.register_next_step_handler(message, user_check)

def start_bot():
    print('Сервер запущен')
    bot.polling(none_stop=True)
