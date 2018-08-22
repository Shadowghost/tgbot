from typing import Optional, List
from googletrans import Translator

from telegram import Update, Bot, ParseMode
from telegram.ext import run_async

from tg_bot import dispatcher
from tg_bot.modules.disable import DisableAbleCommandHandler


@run_async
def gtranslate(bot: Bot, update: Update, args: List[str]):
    msg = update.effective_message  # type: Optional[Message]
    translator = Translator()

    reply_text = msg.reply_to_message.reply_text if msg.reply_to_message else msg.reply_text

    if len(args) == 0 and msg.reply_to_message == None :
        reply_text("Write or quote something to translate.")
        return

    elif len(args) >= 1:
        text = " ".join(args).split(" - ")

    elif msg.reply_to_message.text != None:
        text = msg.reply_to_message.text.split(" - ")

    if len(text) == 2:
        try:
            trans = translator.translate(text[1], dest=text[0]).text
        except ValueError as e:
            reply_text("Language _%s_ not found :(" % text[0], parse_mode=ParseMode.MARKDOWN, quote=True, failed=True)
            return

    else:
        trans = translator.translate(text[0], dest='en').text

    repl = "*Translation:* {}".format(trans)

    reply_text(repl, parse_mode=ParseMode.MARKDOWN, quote=True)


__help__ = """
 - /gtranslate <lang> - <string>:
Type a string of words you want to translate. You can also quote a message instead.
<lang> parameter is optional, default value is *en* for English.
"""


__mod_name__ = "Google Translate"

GTRANSLATE_HANDLER = DisableAbleCommandHandler("gtranslate", gtranslate, pass_args=True)

dispatcher.add_handler(GTRANSLATE_HANDLER)
