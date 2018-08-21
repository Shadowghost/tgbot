import html
from typing import Optional, List
import wikipedia

from telegram import Message, Update, Bot, User, ParseMode, MessageEntity
from telegram.ext import CommandHandler, run_async, Filters, MessageHandler

from tg_bot import dispatcher
from tg_bot.modules.disable import DisableAbleCommandHandler


@run_async
def wiki(bot: Bot, update: Update, args: List[str]):
    msg = update.effective_message  # type: Optional[Message]

    if len(args) == 0 and msg.reply_to_message.text == None :
        update.effective_message.reply_text("Write something you want to look up.")
        return

    elif len(args) >= 1:
        text = " ".join(args)

    elif msg.reply_to_message.text != None:
        text = msg.reply_to_message.text

    try:
        link = wikipedia.page(text).url
        summary = wikipedia.summary(text, sentences=1, auto_suggest=True)

        wiki = "<b>Link:</b> {}" \
               "\n\n" \
               "{}".format(html.escape(link), html.escape(summary))

        reply_text = msg.reply_to_message.reply_text if msg.reply_to_message else msg.reply_text

        reply_text(wiki, parse_mode=ParseMode.HTML, quote=True, disable_web_page_preview=True)

    except:
        update.effective_message.reply_text("No Wikipedia entry found - please try again.")
        return

__help__ = """
 - /wiki <string>: Type a string of words you want to look up on Wikipedia. You can also quote a message instead.
"""


__mod_name__ = "Wikipedia"

WIKI_HANDLER = DisableAbleCommandHandler("wiki", wiki, pass_args=True)

dispatcher.add_handler(WIKI_HANDLER)
