# © TamilBots 2021-22

from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
import youtube_dl
from youtube_search import YoutubeSearch
import requests

import os
from config import Config

bot = Client(
    'SongPlayRoBot',
    bot_token = Config.BOT_TOKEN,
    api_id = Config.API_ID,
    api_hash = Config.API_HASH
)

## Extra Fns -------------------------------

# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


## Commands --------------------------------
@bot.on_message(filters.command(['start']))
def start(client, message):
    TamilBots = f'👋 𝗛𝗲𝗹𝗹𝗼 @{message.from_user.username}\n\n𝙄 𝘼𝙢 𝙕𝙤𝙧𝙤[🎶](https://telegra.ph/file/9c9af363fe39de5442482.mp4)\n\n𝙎𝙚𝙣𝙙 𝙏𝙝𝙚 𝙎𝙖𝙢𝙚 𝙤𝙛 𝙩𝙝𝙚 𝙎𝙤𝙣𝙜𝙨 𝙔𝙤𝙪 𝙬𝙖𝙣𝙩..\n\n𝙏𝙮𝙥𝙚 /s Song name\n\n𝐄𝐠. `/s Rumbling`'
    message.reply_text(
        text=TamilBots, 
        quote=False,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('𝙎𝙐𝙋𝙋𝙊𝙍𝙏 ', url='https://t.me/GodsValley'),
                    InlineKeyboardButton('𝘼𝘿𝘿 𝙈𝙀 ', url='https://t.me/SantoryuROBOT?startgroup=true')
                ]
            ]
        )
    )

@bot.on_message(filters.command(['s']))
def a(client, message):
    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply('🔎 Sᴇᴀʀᴄʜɪɴɢ Tʜᴇ Sᴏɴɢ....')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        # results = YoutubeSearch(query, max_results=1).to_dict()
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]

            ## UNCOMMENT THIS IF YOU WANT A LIMIT ON DURATION. CHANGE 1800 TO YOUR OWN PREFFERED DURATION AND EDIT THE MESSAGE (30 minutes cap) LIMIT IN SECONDS
            # if time_to_seconds(duration) >= 1800:  # duration limit
            #     m.edit("Exceeded 30mins cap")
            #     return

            views = results[0]["views"]
            thumb_name = f'thumb{message.message_id}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:
            print(e)
            m.edit('Fᴏᴜɴᴅ Nᴏᴛʜɪɴɢ. Cʜᴇᴄᴋ Sᴘᴇʟʟɪɴɢ Mɪsᴛᴀᴋᴇs ʙʀᴜʜ')
            return
    except Exception as e:
        m.edit(
            "✖️ Fᴏᴜɴᴅ Nᴏᴛʜɪɴɢ.\n\nFᴏʀ Gᴏᴅs Sᴀᴋᴇ Aᴛʟᴇᴀsᴛ Dᴏ Tʜɪs Rɪɢʜᴛ\n\nEg.`/s Akuma no Ko`"
        )
        print(str(e))
        return
    m.edit("🔎 Fɪɴᴅɪɴɢ Sᴏɴɢ 🎶 Wᴀɪᴛ Fᴏʀ Sᴏᴍᴇ Tɪᴍᴇ [🚀](https://telegra.ph/file/3c2998a28a15d9e09c562.mp4)")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f'🎧 Tɪᴛʟᴇ : [{title[:35]}]({link})\n⏳ Dᴜʀᴀᴛɪᴏɴ : `{duration}`\n🎬 Sᴏᴜʀᴄᴇ : [Youtube](https://youtu.be/3pN0W4KzzNY)\n👁‍🗨 Vɪᴇᴡs : `{views}`\n\n Bʏ : @GodsValley'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, parse_mode='md',quote=False, title=title, duration=dur, thumb=thumb_name)
        m.delete()
    except Exception as e:
        m.edit('❌ Eʀʀᴏʀ\n\n Report This Erorr To Fix @GodsValley ❤️')
        print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

bot.run()
