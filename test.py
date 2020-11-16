
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

import telegram

import io


# bot = telebot.TeleBot(config.token)
bot = telegram.Bot(token=config.token)

media = []

with open('export/thumb2.jpeg', 'rb') as fh:
    buf = io.BytesIO(fh.read())

# media.append(types.InputMediaDocument(media = 'attach://export/cert.pdf2', thumb = 'attach://export/thumb3.jpeg'))
media.append(telegram.InputMediaDocument(media = open('export/cert.pdf2', 'rb'), caption="12", thumb = open('export/thumb2.jpeg', 'rb')))

out = bot.send_media_group(chat_id=config.metelid,media=media)
print(out)