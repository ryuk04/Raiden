import os
import re
import random
from platform import python_version as kontol
from telethon import events, Button
from telegram import __version__ as telever
from telethon import __version__ as tlhver
from pyrogram import __version__ as pyrover
from src.events import register
from src import telethn as tbot

VENOM = (
      "https://graph.org/file/0cee276f2baecdf7df0b9.jpg",
      "https://graph.org/file/79666d9264f849fb06a50.jpg",
)

@register(pattern=("/start"))
async def awake(event):
  TEXT = f"Hey [{event.sender.first_name}](tg://user?id={event.sender.id}), Myself Raiden Shogun- I'm here to help you manage your groups with advance and lots of features!\n\n"
  TEXT += "**Hit /help to find out more about how to use me to my full potential.**"
  BUTTON = [[Button.url("➕Add Me To Your Chat➕", "https://t.me/mikuprorobot?startgroup=true"),]]
  BUTTON+= [[Button.url("Help", "https://t.me/mikuprorobot?startgroup=true"),]]
  await tbot.send_file(event.chat_id, random.choice(VENOM), caption=TEXT, buttons=BUTTON)
