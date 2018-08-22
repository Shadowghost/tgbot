from PyLyrics import *
from telegram import Update, Bot, ParseMode
from telegram.ext import run_async
from typing import Optional, List

from tg_bot.modules.disable import DisableAbleCommandHandler
from tg_bot import dispatcher

from requests import get

LYRICSINFO = "\n\n[Full Lyrics](http://lyrics.wikia.com/wiki/%s:%s)"


@run_async
def lyrics(bot: Bot, update: Update, args: List[str]):
    msg = update.effective_message
    song = " ".join(args).split(" - ")

    reply_text = msg.reply_to_message.reply_text if msg.reply_to_message else msg.reply_text

    if len(song) == 2:
        while song[1].startswith(" "):
            song[1] = song[1][1:]
        while song[0].startswith(" "):
            song[0] = song[0][1:]
        while song[1].endswith(" "):
            song[1] = song[1][:-1]
        while song[0].endswith(" "):
            song[0] = song[0][:-1]
        try:
            lyrics = "\n".join(PyLyrics.getLyrics(
                song[0], song[1]).split("\n")[:10])
        except ValueError as e:
            return reply_text("Song %s not found :(" % song[1], quote=True, failed=True)
        else:
            lyricstext = LYRICSINFO % (song[0].replace(
                " ", "_"), song[1].replace(" ", "_"))
            return reply_text(lyrics + lyricstext, parse_mode=ParseMode.MARKDOWN, quote=True, disable_web_page_preview=True)
    else:
        return reply_text("Invalid syntax - correct syntax:  `/lyrics Artist - Song`", parse_mode=ParseMode.MARKDOWN, quote=True, failed=True)


__help__ = """
 - /lyrics <artist - <song>: Find your favourite songs' lyrics
"""


__mod_name__ = "Lyrics"

LYRICS_HANDLER = DisableAbleCommandHandler("lyrics", lyrics, pass_args=True)

dispatcher.add_handler(LYRICS_HANDLER)
