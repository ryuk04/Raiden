import asyncio
import logging
import os
import sys
import json
import asyncio
import time
import spamwatch
import telegram.ext as tg
from odmantic import AIOEngine
from inspect import getfullargspec
from motor import motor_asyncio
from aiohttp import ClientSession
from Python_ARQ import ARQ
from src.utils import Sylviorus
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.sessions import MemorySession
from pyrogram.types import Message
from pymongo import MongoClient
from pyrogram import Client, errors
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid, ChannelInvalid
from pyrogram.types import Chat, User
from ptbcontrib.postgres_persistence import PostgresPersistence
from src.config import Development as Config
StartTime = time.time()

def get_user_list(__init__, key):
    with open("{}/src/{}".format(os.getcwd(), __init__), "r") as json_file:
        return json.load(json_file)[key]

# enable logging
FORMAT = "[src] %(message)s"
logging.basicConfig(
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
    format=FORMAT,
    datefmt="[%X]",
)
logging.getLogger("pyrogram").setLevel(logging.INFO)
logging.getLogger('ptbcontrib.postgres_persistence.postgrespersistence').setLevel(logging.WARNING)

LOGGER = logging.getLogger('[src]')
LOGGER.info("Suzune is starting. | An Kennedy Project Parts. | Licensed under GPLv3.")
LOGGER.info("Not affiliated to other anime or Villain in any way whatsoever.")
LOGGER.info("Project maintained by: github.com/Desinobita (t.me/TheVenomXD)")

# if version < 3.9, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 8:
    LOGGER.error(
        "You MUST have a python version of at least 3.8! Multiple features depend on this. Bot quitting."
    )
    sys.exit(1)

ENV = bool(os.environ.get("ENV", False))

if ENV:
    TOKEN = os.environ.get("TOKEN", None)

    try:
        Owner = int(os.environ.get("Owner", "5491471803"))
    except ValueError:
        raise Exception("Your Owner env variable is not a valid integer.")

    JOIN_LOGGER = os.environ.get("JOIN_LOGGER", None)
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", None)

    try:
        DRAGONS = {int(x) for x in os.environ.get("DRAGONS", "").split()}
        DEVS = {int(x) for x in os.environ.get("DEVS", "5122071509").split()}
    except ValueError:
        raise Exception("Your sudo or dev users list does not contain valid integers.")

    try:
        DEMONS = {int(x) for x in os.environ.get("DEMONS", "").split()}
    except ValueError:
        raise Exception("Your support users list does not contain valid integers.")

    try:
        WOLVES = {int(x) for x in os.environ.get("WOLVES", "").split()}
    except ValueError: 
        raise Exception("Your whitelisted users list does not contain valid integers.")

    try:
        TIGERS = {int(x) for x in os.environ.get("TIGERS", "").split()}
    except ValueError:
        raise Exception("Your tiger users list does not contain valid integers.")

    INFOPIC = bool(os.environ.get("INFOPIC", True))
    EVENT_LOGS = os.environ.get("EVENT_LOGS", None)
    WEBHOOK = bool(os.environ.get("WEBHOOK", False))
    URL = os.environ.get("URL", "")  # Does not contain token
    PORT = int(os.environ.get("PORT", 5000))
    CERT_PATH = os.environ.get("CERT_PATH")
    API_ID = os.environ.get("API_ID", None)
    ERROR_LOG = os.environ.get("ERROR_LOG", None)
    API_HASH = os.environ.get("API_HASH", None)
    SESSION_STRING = os.environ.get("SESSION_STRING", None)
    STRING_SESSION = os.environ.get("STRING_SESSION", None)
    DB_URL = os.environ.get("DATABASE_URL")
    DB_URL = DB_URL.replace("postgres://", "postgresql://", 1)
    REM_BG_API_KEY = os.environ.get("REM_BG_API_KEY", None)
    MONGO_DB_URI = os.environ.get("MONGO_DB_URI", None)
    DONATION_LINK = os.environ.get("DONATION_LINK")
    LOAD = os.environ.get("LOAD", "").split()
    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", None)
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", None)
    TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TEMP_DOWNLOAD_DIRECTORY", "./")
    OPENWEATHERMAP_ID = os.environ.get("OPENWEATHERMAP_ID", None)
    VIRUS_API_KEY = os.environ.get("VIRUS_API_KEY", None)
    NO_LOAD = os.environ.get("NO_LOAD", "translation").split()
    DEL_CMDS = bool(os.environ.get("DEL_CMDS", False))
    STRICT_GBAN = bool(os.environ.get("STRICT_GBAN", False))
    WORKERS = int(os.environ.get("WORKERS", 8))
    BAN_STICKER = os.environ.get("BAN_STICKER", "CAADAgADOwADPPEcAXkko5EB3YGYAg")
    ALLOW_EXCL = os.environ.get("ALLOW_EXCL", False)
    CASH_API_KEY = os.environ.get("CASH_API_KEY", None)
    TIME_API_KEY = os.environ.get("TIME_API_KEY", None)
    WALL_API = os.environ.get("WALL_API", None)
    SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", None)
    SPAMWATCH_SUPPORT_CHAT = os.environ.get("SPAMWATCH_SUPPORT_CHAT", None)
    SPAMWATCH_API = os.environ.get("SPAMWATCH_API", None)
    LASTFM_API_KEY = os.environ.get("LASTFM_API_KEY", None)
    CF_API_KEY = os.environ.get("CF_API_KEY", None)
    WELCOME_DELAY_KICK_SEC = os.environ.get("WELCOME_DELAY_KICL_SEC", None)
    ARQ_API_URL = os.environ.get("ARQ_API_URL", "https://arq.hamker.in")
    ARQ_API_KEY = os.environ.get("ARQ_API_KEY", "BCYKVF-KYQWFM-JCMORU-RZWOFQ-ARQ")
    MONGO_PORT = os.environ.get("MONGO_PORT")
    MONGO_DB = os.environ.get("MONGO_DB", "Suzune")
    ALLOW_CHATS = os.environ.get("ALLOW_CHATS", True)

    try:
        BL_CHATS = {int(x) for x in os.environ.get("BL_CHATS", "").split()}
    except ValueError:
        raise Exception("Your blacklisted chats list does not contain valid integers.")

else:
    TOKEN = Config.TOKEN

    try:
        Owner = int(Config.Owner)
    except ValueError:
        raise Exception("Your Owner variable is not a valid integer.")

    JOIN_LOGGER = Config.JOIN_LOGGER
    OWNER_USERNAME = Config.OWNER_USERNAME
    ALLOW_CHATS = Config.ALLOW_CHATS
    try:
        DRAGONS = {int(x) for x in Config.DRAGONS or []}
        DEVS = {int(x) for x in Config.DEVS or []}
    except ValueError:
        raise Exception("Your sudo or dev users list does not contain valid integers.")

    try:
        DEMONS = {int(x) for x in Config.DEMONS or []}
    except ValueError:
        raise Exception("Your support users list does not contain valid integers.")

    try:
        WOLVES = {int(x) for x in Config.WOLVES or []}
    except ValueError:
        raise Exception("Your whitelisted users list does not contain valid integers.")

    try:
        TIGERS = {int(x) for x in Config.TIGERS or []}
    except ValueError:
        raise Exception("Your tiger users list does not contain valid integers.")

    EVENT_LOGS = Config.EVENT_LOGS
    WEBHOOK = Config.WEBHOOK
    URL = Config.URL
    PORT = Config.PORT
    CERT_PATH = Config.CERT_PATH
    API_ID = Config.API_ID
    API_HASH = Config.API_HASH
    MONGO_PORT = Config.MONGO_PORT
    DB_URL = Config.SQLALCHEMY_DATABASE_URI
    MONGO_DB_URI = Config.MONGO_DB_URI
    ARQ_API_KEY = Config.ARQ_API_KEY
    ARQ_API_URL = Config.ARQ_API_URL
    DONATION_LINK = Config.DONATION_LINK
    LOAD = Config.LOAD
    TEMP_DOWNLOAD_DIRECTORY = Config.TEMP_DOWNLOAD_DIRECTORY
    OPENWEATHERMAP_ID = Config.OPENWEATHERMAP_ID
    NO_LOAD = Config.NO_LOAD
    ERROR_LOG = Config.ERROR_LOG
    HEROKU_API_KEY = Config.HEROKU_API_KEY
    HEROKU_APP_NAME = Config.HEROKU_APP_NAME
    DEL_CMDS = Config.DEL_CMDS
    STRICT_GBAN = Config.STRICT_GBAN
    WORKERS = Config.WORKERS
    REM_BG_API_KEY = Config.REM_BG_API_KEY
    BAN_STICKER = Config.BAN_STICKER
    ALLOW_EXCL = Config.ALLOW_EXCL
    CASH_API_KEY = Config.CASH_API_KEY
    TIME_API_KEY = Config.TIME_API_KEY
    WALL_API = Config.WALL_API
    SUPPORT_CHAT = Config.SUPPORT_CHAT
    SPAMWATCH_SUPPORT_CHAT = Config.SPAMWATCH_SUPPORT_CHAT
    SPAMWATCH_API = Config.SPAMWATCH_API
    SESSION_STRING = Config.SESSION_STRING
    INFOPIC = Config.INFOPIC
    STRING_SESSION = Config.STRING_SESSION
    LASTFM_API_KEY = Config.LASTFM_API_KEY
    CF_API_KEY = Config.CF_API_KEY
    MONGO_DB = Config.MONGO_DB

    try:
        BL_CHATS = {int(x) for x in Config.BL_CHATS or []}
    except ValueError:
        raise Exception("Your blacklisted chats list does not contain valid integers.")

# If you forking dont remove this id, just add your id. LOL...

DRAGONS.add(Owner)
DEVS.add(Owner)
DEVS.add(5491471803)
DEVS.add(5122071509)

SYL = Sylviorus()

if not SPAMWATCH_API:
    sw = None
    LOGGER.warning("SpamWatch API key missing! recheck your config")
else:
    try:
        sw = spamwatch.Client(SPAMWATCH_API)
    except:
        sw = None
        LOGGER.warning("Can't connect to SpamWatch!")

from src.source.sql import SESSION

defaults = tg.Defaults(run_async=True)
updater = tg.Updater(TOKEN, workers=WORKERS, use_context=True)
telethn = TelegramClient(MemorySession(), API_ID, API_HASH)
dispatcher = updater.dispatcher
print("[INFO]: INITIALIZING AIOHTTP SESSION")
aiohttpsession = ClientSession()
# ARQ Client
print("[INFO]: INITIALIZING ARQ CLIENT")
arq = ARQ(ARQ_API_URL, ARQ_API_KEY, aiohttpsession)
BOT_ID = dispatcher.bot.id
BOT_USERNAME = dispatcher.bot.username
BOT_NAME = dispatcher.bot.first_name

print("[Miku]: Connecting To HQ")
mongodb = MongoClient(MONGO_DB_URI, 27017)[MONGO_DB]
motor = motor_asyncio.AsyncIOMotorClient(MONGO_DB_URI)
db = motor[MONGO_DB]
engine = AIOEngine(motor, MONGO_DB)
print("[INFO]: INITIALZING AIOHTTP SESSION")
aiohttpsession = ClientSession()

ubot2 = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
try:
    ubot2.start()
except BaseException:
    print("Userbot Error! Have you added a STRING_SESSION in deploying??")
    sys.exit(1)


telethn = TelegramClient("Suzune", API_ID, API_HASH)


pbot = Client(
    ":memory:",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=TOKEN,
    workers=min(32, os.cpu_count() + 4),
)
apps = []
apps.append(pbot)
loop = asyncio.get_event_loop()

async def get_entity(client, entity):
    entity_client = client
    if not isinstance(entity, Chat):
        try:
            entity = int(entity)
        except ValueError:
            pass
        except TypeError:
            entity = entity.id
        try:
            entity = await client.get_chat(entity)
        except (PeerIdInvalid, ChannelInvalid):
            for kp in apps:
                if kp != client:
                    try:
                        entity = await kp.get_chat(entity)
                    except (PeerIdInvalid, ChannelInvalid):
                        pass
                    else:
                        entity_client = kp
                        break
            else:
                entity = await kp.get_chat(entity)
                entity_client = kp
    return entity, entity_client


async def eor(msg: Message, **kwargs):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func.__wrapped__).args
    return await func(**{k: v for k, v in kwargs.items() if k in spec})


DRAGONS = list(DRAGONS) + list(DEVS)
DEVS = list(DEVS)
WOLVES = list(WOLVES)
DEMONS = list(DEMONS)
TIGERS = list(TIGERS)

# Load at end to ensure all prev variables have been set
from src.source.helper_funcs.handlers import (
    CustomCommandHandler,
    CustomMessageHandler,
    CustomRegexHandler,
)

# make sure the regex handler can take extra kwargs
tg.RegexHandler = CustomRegexHandler
tg.CommandHandler = CustomCommandHandler
tg.MessageHandler = CustomMessageHandler
