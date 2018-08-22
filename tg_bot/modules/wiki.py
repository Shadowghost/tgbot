from typing import Optional, List
import wikipedia

from telegram import Update, Bot, ParseMode
from telegram.ext import run_async

from tg_bot import dispatcher
from tg_bot.modules.disable import DisableAbleCommandHandler


@run_async
def wiki(bot: Bot, update: Update, args: List[str]):
    msg = update.effective_message  # type: Optional[Message]

    reply_text = msg.reply_to_message.reply_text if msg.reply_to_message else msg.reply_text

    if len(args) == 0 and msg.reply_to_message == None :
        reply_text("Write something you want to look up.")
        return

    elif len(args) >= 1:
        text = " ".join(args).split(" - ")

    elif msg.reply_to_message.text != None:
        text = msg.reply_to_message.text.split(" - ")

    if len(text) == 2:
        try:
            wikipedia.set_lang(text[0])
            link = wikipedia.page(text[1]).url
            summary = wikipedia.summary(text[1], sentences=1, auto_suggest=True)

            wiki = "{}" \
                   "\n\n" \
                   "*Link:* {}".format(summary, link)

            reply_text(wiki, parse_mode=ParseMode.MARKDOWN, quote=True, disable_web_page_preview=True)

        except:
            reply_text("No Wikipedia entry found - please try again.", quote=True, failed=True)
            return
    else:
        try:
            wikipedia.set_lang('en')
            link = wikipedia.page(text[0]).url
            summary = wikipedia.summary(text[0], sentences=1, auto_suggest=True)

            wiki = "*Link:* {}" \
                   "\n\n" \
                   "{}".format(link, summary)

            reply_text(wiki, parse_mode=ParseMode.MARKDOWN, quote=True, disable_web_page_preview=True)

        except:
            reply_text("No Wikipedia entry found - please try again.", quote=True, failed=True)
            return


__help__ = """
 - /wiki <lang> - <string>:
Type a string of words you want to look up on Wikipedia. You can also quote a message instead.
<lang> parameter is optional, default value is *en* for English.
"""


__mod_name__ = "Wikipedia"

WIKI_HANDLER = DisableAbleCommandHandler("wiki", wiki, pass_args=True)

dispatcher.add_handler(WIKI_HANDLER)
