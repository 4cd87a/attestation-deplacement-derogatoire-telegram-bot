# -*- coding: utf-8 -*-
import os, time
from datetime import datetime
pth = os.path.abspath(__file__)
pth = os.path.dirname(pth)
print(pth)
import telebot
import traceback

from telebot import types
from core import core
import config

bot = telebot.TeleBot(config.token)

print("Im in")

def zabs(i):
    if int(i)<0: return 0
    else: return i


@bot.message_handler(commands=['start'])
def handle_start(message):
    if message.chat.type == 'supergroup' or message.chat.type == 'group':
        return True

    mess = "Hi"
    cor = core(message.from_user.id)
    if cor.user is None:
        cor.db.user_add(telid=message.from_user.id,telusername=message.from_user.username,mode=1)
        bot.send_message(message.chat.id, "Hi! Write your name in format:\nPrenom NOM")
    else:
        bot.send_message(message.chat.id, "Hi again. You are already in the system. Use /edit to edit your personal info.")

    cor.log_save(mess="New user",typ=0)
    cor.close()

@bot.message_handler(commands=['exit'])
def handle_exit(message):
    if message.chat.type == 'supergroup' or message.chat.type == 'group': return True
    cor = core(message.from_user.id)
    cor.db.user_set_mode()
    bot.send_message(message.chat.id, "Exited")
    cor.close()

@bot.message_handler(commands=['edit'])
def handle_edit(message):
    if message.chat.type == 'supergroup' or message.chat.type == 'group': return True
    cor = core(message.from_user.id)
    cor.db.user_set_mode(mode=1)
    bot.send_message(message.chat.id, "You're about to edit personal information. Rewrite your name in format:\nPrenom NOM\nIf you want to change nothing send /exit")
    cor.close()

@bot.message_handler(commands=['travail', 'achats', 'sante', 'famille', 'handicap', 'sport', 'convocation', 'missions', 'enfants'])
def handle_command(message):
    if message.chat.type == 'supergroup' or message.chat.type == 'group': return True

    try: #if True:
        cor = core(message.from_user.id)
        data = cor.command(message.text, message.message_id)
        sent_info = send(data=data, to=message.chat.id)
        cor.close(data=data,sent_info=sent_info,mode='command')

    except Exception as e:
        print("Error: ".format(e))
        with open('log.txt', 'a') as f:
            f.write('---------- {} {} ----------'.format(int(time.time()),datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
            f.write("{}\n".format(cor.logs))
            f.write(str(e))
            f.write(traceback.format_exc())
        bot.reply_to(message, e)
        bot.send_message(config.metelid, e, disable_notification=False)
        cor.log_save(typ=2)

@bot.message_handler(commands=['feedback'])
def handle_feedback(message):
    if message.chat.type == 'supergroup' or message.chat.type == 'group': return True
    bot.forward_message(config.metelid, message.chat.id, message.message_id)
    bot.reply_to(message, "done")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    if message.chat.type == 'supergroup' or message.chat.type == 'group': return True
    if message.caption=='/feedback':
        bot.forward_message(config.metelid, message.chat.id, message.message_id)
        bot.reply_to(message, "done")
    else:
        bot.reply_to(message, "If you want to send this photo to me, use `/feedback` as a caption for photo")

@bot.message_handler(commands=['toall'])
def handle_edit(message):
    if message.chat.type == 'supergroup' or message.chat.type == 'group': return True
    try:
        cor = core(message.from_user.id)
        users, data = cor.toall(message.text, message.message_id)
        for user in users:
            sent_info = send(data=data, to=user)

        cor.close(data=data, sent_info=sent_info,mode='toall')

    except Exception as e:
        print("Error: ".format(e))
        with open('log.txt', 'a') as f:
            f.write('---------- {} {} ----------'.format(int(time.time()),datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
            f.write("{}\n".format(cor.logs))
            f.write(str(e))
            f.write(traceback.format_exc())
        bot.reply_to(message, e)
        bot.send_message(config.metelid, e, disable_notification=False)
        cor.log_save(typ=4)

@bot.message_handler(commands=['test'])
def handle_edit(message):
    if message.chat.type == 'supergroup' or message.chat.type == 'group': return True

    cor = core(message.from_user.id)
    data = cor.test(message.text, message.message_id)
    cor.close()


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе
    #if True:
    try:
        cor = core(message.from_user.id)
        data = cor.text(message.text, message.message_id)
        sent_info = send(data=data, to=message.chat.id)
        cor.close(data=data, sent_info=sent_info,mode='text')

    except Exception as e:
        print("Error: ".format(e))
        with open('log.txt', 'a') as f:
            f.write('---------- {} {} ----------'.format(int(time.time()),datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
            f.write("{}\n".format(cor.logs))
            f.write(str(e))
            f.write(traceback.format_exc())
        bot.reply_to(message, e)
        bot.send_message(config.metelid, e, disable_notification=False)
        cor.log_save(typ=3)



def send(data=None,to=None, messId=None, disable_notification=False):
    if to==None: return False #to=me
    mess = data.get('mess',None)
    photo = data.get('photo',None)
    file = data.get('file',None)
    if messId==None: messId=data.get('messId',None)

    out = None

    if photo!=None:
        if messId==None:
            if type(photo)==list:
                media = []
                for i, p in enumerate(photo):
                    if i==0:
                        media.append(types.InputMediaPhoto(open(p, 'rb'), caption=mess))
                    else:
                        media.append(types.InputMediaPhoto(open(p, 'rb')))

                out = bot.send_media_group(chat_id=to,media=media)
            else:
                out = bot.send_photo(to, open(photo, 'rb'), caption=mess, disable_notification=disable_notification)
        else:
            if type(photo) == list:
                if type(messId)==list and len(photo)==len(messId):
                    for i, p in enumerate(photo):
                        if i==0:
                            out = bot.edit_message_media(chat_id=to, message_id=messId[i],
                                media=types.InputMediaPhoto(open(p, 'rb'), caption=mess))
                        else:
                            out = bot.edit_message_media(chat_id=to, message_id=messId[i],
                                 media=types.InputMediaPhoto(open(p, 'rb')))

                else:
                    print("if photo is list then messId should be also a list of the same size")
            else:
                out = bot.edit_message_media(chat_id=to, message_id=messId,
                                media=types.InputMediaPhoto(open(photo, 'rb'), caption=mess))

    if file!=None:
        if messId == None:
            if type(file)==list:
                media = []
                for i, p in enumerate(file):
                    if i==0:
                        media.append(types.InputMediaDocument(open(p, 'rb'), caption=mess))
                    else:
                        media.append(types.InputMediaDocument(open(p, 'rb')))

                out = bot.send_media_group(chat_id=to,media=media)
            else:
                out = bot.send_document(to, open(file, 'rb'), caption=mess, disable_notification=disable_notification)
        else:
            if type(file) == list:
                if type(messId)==list and len(file)==len(messId):
                    for i, p in enumerate(file):
                        if i==0:
                            out = bot.edit_message_media(chat_id=to, message_id=messId[i],
                                media=types.InputMediaDocument(open(p, 'rb'), caption=mess))
                        else:
                            out = bot.edit_message_media(chat_id=to, message_id=messId[i],
                                 media=types.InputMediaDocument(open(p, 'rb')))

                else:
                    print("if photo is list then messId should be also a list of the same size")
            else:
                out = bot.edit_message_media(chat_id=to, message_id=messId,
                                media=types.InputMediaDocument(open(file, 'rb'), caption=mess))


    elif mess!=None:
        if messId==None:
            out = bot.send_message(to,mess, disable_notification=disable_notification)
        else:
            #print(mess,to,messId)
            out = bot.edit_message_text(text=mess,chat_id=to,message_id=messId)
    #print(out)
    if type(out)==list:
        return [o.message_id for o in out]

    return out.message_id

if __name__ == '__main__':
    if True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print("{!s}\n{!s}".format(type(e), str(e)))
        print("rebout")