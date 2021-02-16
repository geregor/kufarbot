from typing import re
import requests
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent
import re
import telebot
import keyboards as kb
from telebot import types
import sqlite3
mass = []
massiv = []
pos = {}
mos = {}
kos = {}
moos = []
los = {}
conn = sqlite3.connect('kufar.db')
bot = telebot.TeleBot("1685702621:AAGr22uWJGIgC-40uVp3q0ayfpxpFNgLy1Q")
message_id = 0
@bot.message_handler ( commands=[ 'start' ] )
def bb(message):
    user_id = message.chat.id
    with sqlite3.connect ( 'kufar.db' ) as conn :
        cursor = conn.cursor()
        cursor.execute(f"SELECT reg FROM sett WHERE user_id = {user_id}")
        qq = cursor.fetchone()
        if qq == None:
            msg = bot.send_message(user_id, 'Привет мой друг, я Kufar бот. Для дальнейшего пользования ботом введите ключ', reply_markup=kb.dbut)
            bot.register_next_step_handler ( msg , second_room )
        else:
            msg = bot.send_message(user_id, "С возвращением!", reply_markup=kb.main)
            bot.register_next_step_handler(msg, main_room)

def second_room(message):
    user_id = message.chat.id
    text = message.text
    if text == 'У меня нету ключа':
        msg = bot.send_message(user_id,"Обратитесь к создателю бота!")
        bot.register_next_step_handler(msg, second_room)
    elif text == 'Пакепачи':
        msg = bot.send_message(user_id,"Ключ верный, приятного использования.", reply_markup=kb.main)
        bot.register_next_step_handler(msg, main_room)
        with sqlite3.connect ( 'kufar.db' ) as conn :
            cursor = conn.cursor ()
            cursor.execute ( f"SELECT user_id FROM sett WHERE user_id={user_id}" )
            if cursor.fetchone () == None :
                cursor.execute ( f"INSERT INTO sett(user_id,reg) VALUES({user_id},1)" )
                conn.commit ()
    else:
        msg = bot.send_message(user_id,"Неверный ключ!")
        bot.register_next_step_handler(msg, second_room)

def main_room(message):
    user_id = message.chat.id
    text = message.text
    if text == "Найти халяву":
        msg = bot.send_message(user_id, "Выбери категорию для халявы", reply_markup=kb.first_but)
        bot.register_next_step_handler(msg, find_1)
    elif text == "Ожидание халявы":
        msg = bot.send_message(user_id, "В разработке", reply_markup=kb.main)
        bot.register_next_step_handler(msg, main_room)
        #msg = bot.send_message(user_id, "Выберите категорию.", reply_markup=kb.fisrt_but)
        #bot.register_next_step_handler(msg, waiting)
    elif text == "Избранное":
        with sqlite3.connect ( 'kufar.db' ) as conn :
            cursor = conn.cursor()
            cursor.execute(f"SELECT what FROM favorite WHERE user_id = {user_id}")
            qq = cursor.fetchall()
            mos[user_id] = 0
            if qq == []:
                msg = bot.send_message(user_id, "У вас пока нету избранных товаров!")
                bot.register_next_step_handler(msg, main_room)
            else:
                
                for k in qq:
                    moos.append(k[0])
            num = len(moos)
            msg = bot.send_message(user_id, "Найдено "+str(num)+" в избранном\n"+str(mos[user_id]+1)+". "+str(moos[mos[user_id]]), reply_markup=kb.buut)
            kos[user_id]=msg.message_id
    else:
        msg = bot.send_message(user_id, "Я не понимаю, используйте клавиатуру")
        bot.register_next_step_handler(msg, main_room)


def find_1(message):
    user_id = message.chat.id
    text = message.text
    with sqlite3.connect ('kufar.db') as conn :
        cursor = conn.cursor ()
        c = False
        if text == "Легкая техника":
            cursor.execute(f"UPDATE sett SET find = 1 WHERE user_id = {user_id}")
            c = True
        elif text == "Тяжелая техника":
            cursor.execute(f"UPDATE sett SET find = 2 WHERE user_id = {user_id}")
            c = True
        elif text == "Одежда(жен)":
            cursor.execute(f"UPDATE sett SET find = 3 WHERE user_id = {user_id}")
            c = True
        elif text == "Приставки":
            cursor.execute(f"UPDATE sett SET find = 4 WHERE user_id = {user_id}")
            c = True
        elif text == "Вернуться в меню":
            msg = bot.send_message(user_id, "Вы вернулись в меню.", reply_markup=kb.main)
            bot.register_next_step_handler(msg,main_room)
        else:
            msg = bot.send_message(user_id, "Я не понимаю, используйте клавиатуру.")
            bot.register_next_step_handler(msg, find_1)
        if c == True:
            conn.commit()
            msg = bot.send_message ( user_id , f"Вы выбрали '{text}'\nВыберите ценовой промежуток, пример 10-40, пробелы и 'Р' не нужны. Можно просто 40." )
            bot.register_next_step_handler(msg, seach_toom)

def seach_toom(message):
    user_id = message.chat.id
    text = message.text
    text = text.replace(' ', '')
    start = 0
    end = 100
    c = False
    try:
        if re.search(r'-', text) != None:
            start = re.split(r'-', text)[0]
            end = re.split(r'-', text)[1]
        if int(end) > int(start):
            msg = bot.send_message(user_id, "Вы выбрали промежуток "+str(start)+" - "+str(end)) #,reply_markup=kb.ww)
            with sqlite3.connect ( 'kufar.db' ) as conn :
                cursor = conn.cursor ()
                cursor.execute(f"UPDATE sett SET money = '{start}-{end}' WHERE user_id = {user_id}")
                conn.commit()
            #bot.register_next_step_handler(msg, toom)
            c = True
        else:
            msg = bot.send_message(user_id, "Выбран не верный промежуток, 2-ое число должно быть больше 1-ого!")
            bot.register_next_step_handler(msg, seach_toom)

    except:
        msg = bot.send_message(user_id, "Произошло недопонимание №100")
        bot.register_next_step_handler(msg, seach_toom)

#def toom(message):
    if c == True:
        user_id = message.chat.id
        text = message.text
        with sqlite3.connect ( 'kufar.db' ) as conn :
            cursor = conn.cursor()
            cursor.execute(f"SELECT find FROM sett WHERE user_id = {user_id}")
            qq = cursor.fetchone()
            for a in qq:
                kom = a
            cursor.execute(f"SELECT money FROM sett WHERE user_id = {user_id}")
            qq = cursor.fetchone()
            for a in qq:
                sum = a
        print(sum)
        sum = re.split(r'-', sum)
        if kom == 1:
            link = 'https://baraholka.onliner.by/search.php?type=lastposts&time=86400&r=1&cat=1'
        elif kom == 2:
            link = 'https://baraholka.onliner.by/search.php?type=lastposts&time=86400&r=2&cat=1'
        elif kom == 3:
            link = 'https://baraholka.onliner.by/search.php?type=lastposts&time=86400&r=571&cat=1'
        elif kom == 4:
            link = 'https://baraholka.onliner.by/search.php?type=lastposts&time=86400&r=4&cat=1'
        r = requests.get(link)
        soup = BS ( r.content , 'html.parser' )

        for i in soup.findAll ( 'div' , class_='m-title' ) :
            b = i.text
            b = b.replace ( 'Новое за 24 часа(найдено ' , '' )
            b = b.replace ( ' объявлений)' , '' )
            b = b.replace ( ' объявления)' , '' )
            b = b.replace ( ' объявление)' , '' )
            kkk = b
        #bot.send_message(user_id, "Найдено " + b + " новых товаров за 24 часа" )
        collichestvo = 0
        collichestvo = divmod ( int ( b ) , 50 ) [ 0 ]
        print ( collichestvo )
        call = 0
        mass = [ ]
        for i in range ( collichestvo ) :
            r = requests.get ( link + "&start=" + str ( call ) )
            call += 50
            soup = BS ( r.content , 'html.parser' )
            for q in soup.findAll('tr'):

                for o in q.findAll('td', class_='frst ph colspan'):
                    for b in o.findAll ( 'h2' , class_='wraptxt' ) :
                        for a in b.findAll ( 'a' ) :
                            klink =  a.get ( 'href' )
                            opis = a.text

                            for b in q.findAll('div', class_='price-primary'):
                                man = re.split ( r',' , b.text ) [ 0 ]
                                man = man.replace(' ', '')
                                if int ( sum [ 0 ] ) <= int ( man ) <= int ( sum [ 1 ] ) :
                                    red = "https://baraholka.onliner.by"+klink+"\nЦена "+b.text+"\n"+opis
                                    #print(red)
                                    massiv.append(red)
        bot.send_message(user_id, "Найдено " + kkk + " новых товаров за 24 часа\nПо заданным фильтрам найдено "+str(len(massiv))  )   
        red = bot.send_message(user_id, massiv[0], reply_markup=kb.butt)
        message_id = red.message_id
        pos[user_id] = 0



@bot.callback_query_handler ( func=lambda call : True )
def get_call(call) :
    user_id = call.message.chat.id
    message_id = call.message.message_id
    if 'mm' in call.data :
        msg = bot.send_message(chat_id=user_id, text="Вы вернулись в меню.", reply_markup=kb.main)
        bot.register_next_step_handler(msg, main_room)
        massiv.clear()
    elif 'dd' in call.data:
        try:
            pos [ user_id ] += 1
            bot.edit_message_text(chat_id=user_id, message_id=message_id, text=massiv [ pos [ user_id  ] ])
            bot.edit_message_reply_markup(chat_id=user_id, message_id=message_id, reply_markup=kb.butt)
        except IndexError:
            pos [ user_id ] = 1
            bot.send_message(user_id, "Товары в данной ценовой категории закончились")
            bot.send_message ( user_id , massiv [ pos [ user_id  ] ] , reply_markup=kb.butt )
    elif 'nn' in call.data:
        try:
            pos [ user_id ] -= 1
            bot.edit_message_text(chat_id=user_id, message_id=message_id, text=massiv [ pos [ user_id  ] ])
            bot.edit_message_reply_markup ( chat_id=user_id , message_id=message_id , reply_markup=kb.butt )
        except IndexError:
            pos [ user_id ] = 1
            bot.send_message(user_id, "Здесь нету товара")
            bot.send_message ( user_id , massiv [ pos [ user_id  ] ] , reply_markup=kb.butt )
    elif 'is' in call.data:
        with sqlite3.connect ( 'kufar.db' ) as conn :
            cursor = conn.cursor ()
            cursor.execute ( f"SELECT what FROM favorite WHERE user_id={user_id}" )
            qq = cursor.fetchall ()
            madiv = []
            for k in qq:
                madiv.append(k[0])
            if massiv[pos[user_id]] not in madiv:
                cursor.execute (f"INSERT INTO favorite (user_id,what) VALUES ({user_id}, '{massiv [ pos [ user_id ] ]}')" )
                bot.send_message ( user_id , "Товар добавлен в избранное")
            else:
                bot.send_message ( user_id , "Данный товар уже находится в избранных" )
            conn.commit()

    elif 'nf' in call.data:
        if mos[user_id] != 0:
            try:
                mos[user_id] -= 1
                message_id = kos[user_id]
                bot.edit_message_text(chat_id=user_id, message_id=message_id, text=str(mos[user_id]+1)+". "+str(moos[mos[user_id]]))
                bot.edit_message_reply_markup(chat_id=user_id, message_id=message_id , reply_markup=kb.buut)
            except:
                bot.send_message(user_id,"Произошло недопонимание №254")
        else:
            bot.send_message(user_id, "Тут нет ничего!")

    elif 'yd' in call.data:
        with sqlite3.connect ( 'kufar.db' ) as conn :
            cursor = conn.cursor ()
            cursor.execute(f"DELETE FROM favorite WHERE what ='{moos[mos[user_id]]}'")
            conn.commit()
            print(len(moos))
            if len(moos) < 1: #1
                msg = bot.send_message(user_id, "Данный товар удален из списка избранных. В избранных больше нету товаров!", kb.main)
                moos.pop(mos[user_id])
                bot.register_next_step_handler(msg, main_room)
            elif (mos[user_id]+1) == len(moos):
                bot.send_message(user_id, "Данный товар удален из списка избранных. #2")
                moos.pop(mos[user_id])
                mos[user_id] -= 1
                bot.edit_message_text(chat_id=user_id, message_id=message_id, text=str(mos[user_id]+1)+". "+str(moos[mos[user_id]]))
                bot.edit_message_reply_markup(chat_id=user_id, message_id=message_id , reply_markup=kb.buut)
            elif (mos[user_id]+1) == 1:
                moos.pop(mos[user_id])
                bot.send_message(user_id, "Данный товар удален из списка избранных. #3")
                mos[user_id] += 1
                bot.edit_message_text(chat_id=user_id, message_id=message_id, text=str(mos[user_id]+1)+". "+str(moos[mos[user_id]]))
                bot.edit_message_reply_markup(chat_id=user_id, message_id=message_id , reply_markup=kb.buut)
            else:
                moos.pop(mos[user_id])
                bot.send_message(user_id, "Данный товар удален из списка избранных. #4")
                mos[user_id] -= 1
                bot.edit_message_text(chat_id=user_id, message_id=message_id, text=str(mos[user_id]+1)+". "+str(moos[mos[user_id]]))
                bot.edit_message_reply_markup(chat_id=user_id, message_id=message_id , reply_markup=kb.buut)

    elif 'df' in call.data:
        if (mos[user_id]+1) != (len(moos)):
            mos[user_id] += 1
            message_id = kos[user_id]
            bot.edit_message_text(chat_id=user_id, message_id=message_id, text=str(mos[user_id]+1)+". "+str(moos[mos[user_id]]))
            bot.edit_message_reply_markup(chat_id=user_id, message_id=message_id , reply_markup=kb.buut)
        else:
            bot.send_message(user_id, "Тут нет ничего!")

def waiting(message):
    user_id = message.chat.id
    text = message.text

if __name__ == '__main__' :
    bot.infinity_polling ()