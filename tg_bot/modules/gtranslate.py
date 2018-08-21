import html
from typing import Optional, List
from googletrans import Translator

from telegram import Message, Update, Bot, User, ParseMode, MessageEntity
from telegram.ext import CommandHandler, run_async, Filters, MessageHandler

from tg_bot import dispatcher
from tg_bot.modules.disable import DisableAbleCommandHandler


@run_async
def gtranslate(bot: Bot, update: Update, args: List[str]):
    msg = update.effective_message  # type: Optional[Message]
    translator = Translator()

    if len(args) == 0 and msg.reply_to_message.text == None :
        update.effective_message.reply_text("Write something to translate.")
        return

    elif len(args) >= 1:
        text = " ".join(args)

    elif msg.reply_to_message.text != None:
        text = msg.reply_to_message.text

    trans = translator.translate(text, dest='en').text
    reply_text = msg.reply_to_message.reply_text if msg.reply_to_message else msg.reply_text

    repl = "<b>Translation:</b> {}".format(html.escape(trans))

    reply_text(repl, parse_mode=ParseMode.HTML, quote=True)


__help__ = """
 - /gtranslate <string>: Type a string of words you want to translate to English. You can also quote a message instead.
"""


__mod_name__ = "Google Translate"

GTRANSLATE_HANDLER = DisableAbleCommandHandler("gtranslate", gtranslate, pass_args=True)

dispatcher.add_handler(GTRANSLATE_HANDLER)
