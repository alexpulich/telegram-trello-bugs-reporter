import telegram
from telegram.ext import BaseFilter

from functools import wraps

import settings
import database
from trello_wrapper import client


def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        if str(user_id) != settings.ADMIN:
            bot.send_message(chat_id=update.message.chat_id,
                             text=settings.ACCESS_DENIED)
            return
        return func(bot, update, *args, **kwargs)

    return wrapped


def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(*args, **kwargs):
        bot, update = args
        bot.send_chat_action(
            chat_id=update.effective_message.chat_id,
            action=telegram.ChatAction.TYPING)
        return func(bot, update, **kwargs)

    return command_func


def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def get_list(update):
    list_id = database.get_list(update.message.chat_id)
    if not list_id:
        update.message.reply_text('Please, config a board and a list first!')
        return False

    trello_list = client.get_list(list_id)
    if not trello_list:
        update.message.reply_text('Failed to retrieve your list from trello!')
        return False

    return trello_list


class BugsFilter(BaseFilter):
    def filter(self, message):
        return '#bugs' in message.text or '#bug' in message.text


bugs_filter = BugsFilter()
