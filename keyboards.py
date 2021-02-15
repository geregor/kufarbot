import telebot
from telebot import types

dbut = types.ReplyKeyboardMarkup( one_time_keyboard=True, resize_keyboard=True)
donate_button = types.KeyboardButton("У меня нету ключа")
dbut.add(donate_button)

back_button = types.KeyboardButton("Вернуться в меню")

main = types.ReplyKeyboardMarkup( one_time_keyboard=True, resize_keyboard=True)
main_seach_b = types.KeyboardButton("Найти халяву")
main_wait_b = types.KeyboardButton("Ожидание халявы")
main_favor_b = types.KeyboardButton("Избранное")
main.add(main_seach_b).add(main_wait_b).add(main_favor_b)

but_1 = types.KeyboardButton("Легкая техника")
but_2 = types.KeyboardButton("Тяжелая техника")
but_3 = types.KeyboardButton("Одежда(жен)")
but_4 = types.KeyboardButton("Приставки")
first_but = types.ReplyKeyboardMarkup( one_time_keyboard=True, resize_keyboard=True)
first_but.add(but_1).add(but_2).add(but_3).add(but_4).add(back_button)

butt = types.InlineKeyboardMarkup()
butt_1 = types.InlineKeyboardButton(text='Далее', callback_data='dd')
butt_2 = types.InlineKeyboardButton(text='В меню', callback_data='mm')
butt_3 = types.InlineKeyboardButton(text='Назад', callback_data='nn')
butt_4 = types.InlineKeyboardButton(text='В избранное', callback_data='is')
butt.add(butt_3,butt_2,butt_1).add(butt_4)

buut = types.InlineKeyboardMarkup()
buut_n = types.InlineKeyboardButton(text="Назад", callback_data='nf')
buut_s = types.InlineKeyboardButton(text="Удалить из избранных", callback_data='yd')
buut_d = types.InlineKeyboardButton(text="Далее", callback_data='df')
buut.add(buut_n,butt_2,buut_d).add(buut_s)


ww = types.ReplyKeyboardMarkup( one_time_keyboard=True, resize_keyboard=True)
ww1 = types.KeyboardButton('')
ww.add(ww1)
#back_button = types.KeyboardButton("Назад")

#reg_keyboard = types.ReplyKeyboardMarkup( one_time_keyboard=True, resize_keyboard=True)
#reg_yes_or_no = types.ReplyKeyboardMarkup( one_time_keyboard=True, resize_keyboard=True)
#reg_button = types.KeyboardButton("Регистрация")
#reg_reloginA = types.KeyboardButton("Да")
#reg_reloginB = types.KeyboardButton("Нет")

#reg_yes_or_no.add(reg_reloginA,reg_reloginB)
##reg_keyboard.add(reg_button)

#mein_meny_keybord = types.ReplyKeyboardMarkup( one_time_keyboard=True, resize_keyboard=True)
#creat_group_button = types.KeyboardButton("Создать группу ➕")
#find_group_button = types.KeyboardButton("Найти группу 🔍")
#mein_meny_keybord.add(find_group_button).add(creat_group_button)