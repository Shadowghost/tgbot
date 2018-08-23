from typing import Optional, List

from telegram import Message, Update, Bot, ParseMode, MessageEntity
from telegram.ext import run_async, CommandHandler

from tg_bot import dispatcher
from tg_bot.modules.helper_funcs.filters import CustomFilters


@run_async
def send_to_channel(bot: Bot, update: Update, args: List[str]):
    msg = update.effective_message  # type: Optional[Message]

    if len(args) <= 1 and msg.reply_to_message == None :
        msg.reply_to_message.reply_text("Quote something you want to post on a channel.")
        return

    elif msg.reply_to_message.text != None:
        channel = " ".join(args)
        text = msg.reply_to_message.text

    try:
        bot.sendMessage(channel, text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
    except:
        msg.reply_to_message.reply_text("An error ocurred while processing your message. Check your formatting.", quote=True, failed=True)
        return


__help__ = """
 - /s2channel <channel>: Reply this to a message on a private chat to send the message to a channel.
"""


__mod_name__ = "Send to channel"

S2CHANNEL = CommandHandler("s2channel", send_to_channel, pass_args=True, filters=CustomFilters.sudo_filter | CustomFilters.secret_sudo_filter)

dispatcher.add_handler(S2CHANNEL)