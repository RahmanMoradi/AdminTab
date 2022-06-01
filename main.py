
from pyrogram.raw import functions
from pyrogram.types import Message
from pyrogram import Client, filters
from datetime import datetime
from redis import Redis
from time import sleep, time
import json
import pytz

# -- The bot port --
port = input("Enter The Port: ")

api_id =   1167061
api_hash = "4de49642ae630ae385b6c10faa7155be"


# -- DataBase --
r = Redis(
    "localhost",
    6379,
    decode_responses=True
)

proxy = {
    "scheme": "socks5",  # "socks4", "socks5" and "http" are supported
    "hostname": "127.0.0.1",
    "port": 9050,
    "username": "1",
    "password": "1"
}
# -- Pyrogram Client -- 
app = Client(
    "Loe"+port,
    api_id,
    api_hash,
    proxy=proxy
)


# -- Check the timer Function -- 
def match_time():

    regoin = pytz.timezone('Asia/Tehran')
    now = datetime.now(regoin).strftime("%H:%M")

    if now == str(Time()):
        return True

    else:
        return False


# -- dataBase Variables --


def Time(): return r.hmget(port, "time")[0]

def Word(): return str(r.hmget(port, "word")[0])

def ChannelNotDelete(): return int(r.hmget(port, "channel")[0])

# --- Handlers ---


# -- ping --
@app.on_message(filters.command("ping") & filters.me)
async def ping(c:Client, m:Message):

    await m.edit("Bot Is Online!")




# -- time --
@app.on_message(filters.command("time") & filters.me)
async def time_handler(c:Client, m:Message):

    text = m.text.split()

    if len(text) == 2:

        r.hmset(port, {"time": text[1]})
        await m.edit(f"Time Seted On {Time()}")

    else :
        await m.edit("ERROR!")




# -- wordSet -- 
@app.on_message(filters.command("word") & filters.me)
async def word_handler(c:Client, m:Message):

    text = m.text.split()

    if len(text) == 2:

        r.hmset(port, {"word": text[1]})
        await m.edit(f"Word Seted On {Word()}")

    else :
        await m.edit("ERROR!")




# -- channelSet --
@app.on_message(filters.command("channel") & filters.me)
async def channel_handler(c:Client, m:Message):

    text = m.text.split()

    if len(text) == 2:

        r.hmset(port, {"channel": text[1]})
        await m.edit(f"Channel Seted On {ChannelNotDelete()}")

    else :
        await m.edit("ERROR!")





# -- startDelete --
@app.on_message()
async def deleteing(c:Client, m:Message):
    if match_time() == True: # Check the time to start deleteing
        f_time = time()
        reg = pytz.timezone('Asia/Tehran')
        oldTime = datetime.now(reg).strftime("%H:%M")

        r.hmset(port, {"time": 0})

        await app.send_message("me", "آغاز عملیات حذف")

        async for message in app.search_global(Word()): # Get messages
            sender = message.sender_chat

            if sender != None:
                
                if sender["type"] == "channel": # Check if message sended from a channel

                    if sender["id"] != ChannelNotDelete(): # Check to not delete the message from channel who don't must delete

                        try:

                            chat_id = sender["id"]
                            message_id = message.message_id

                            await app.delete_messages(chat_id=chat_id, message_ids=message_id) # Delete the message

                        except Exception as a:
                            print(a)
        
        r.hmset(port, {"time": oldTime})

        await app.send_message(
            "me",
            f"اتمام عملیات حذف\nمدت زمان {int(time() - f_time)} ثانیه"
        )

        sleep(60) # sleep one minute for not runing the deleting again ! 

app.run()

