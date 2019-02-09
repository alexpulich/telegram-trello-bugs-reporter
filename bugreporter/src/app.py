from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler
from telegram.ext import Filters, Updater
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import settings
from trello_wrapper import client
import utils
import database

REQUEST_KWARGS = {}

if settings.PROXY:
    REQUEST_KWARGS['proxy_url'] = settings.PROXY


@utils.send_typing_action
def start(bot, update):
    """
    /start telegram command handler
    Shows just simple welcome message

    :param bot:
    :param update:
    :return:
    """
    bot.send_message(
        chat_id=update.message.chat_id,
        text=settings.START_TEXT
    )


@utils.send_typing_action
@utils.restricted
def config(bot, update):
    """
    /config telegram command. Needed to set up required Trello board and list
    :param bot:
    :param update:
    :return:
    """
    boards = client.list_boards()
    button_list = []
    for board in boards:
        button_list.append(
            InlineKeyboardButton(board.name, callback_data=f'bid{board.id}')
        )

    reply_markup = InlineKeyboardMarkup(
        utils.build_menu(button_list, n_cols=2)
    )
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Please, choose a board",
        reply_markup=reply_markup
    )


@utils.send_typing_action
def button(bot, update):
    """
    Handler for inline keyboards provoked by /config command

    :param bot:
    :param update:
    :return:
    """
    query = update.callback_query

    if query.data.startswith('bid'):
        configuration = {
            'board': query.data[3:],
            'chat_id': query.message.chat_id
        }

        database.save_config(configuration)

        bugs_board = client.get_board(query.data[3:])
        lists = bugs_board.all_lists()

        button_list = []
        for lst in lists:
            button_list.append(
                InlineKeyboardButton(lst.name, callback_data=f'lid{lst.id}')
            )

        reply_markup = InlineKeyboardMarkup(
            utils.build_menu(button_list, n_cols=2)
        )

        bot.edit_message_text(text='Now, please, choose a list',
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=reply_markup)

    elif query.data.startswith('lid'):
        configuration = {
            'list': query.data[3:],
            'chat_id': query.message.chat_id
        }

        database.save_config(configuration)

        bot.send_message(
            chat_id=query.message.chat_id,
            text=f'Congrats! You are ready to report bugs!'
        )
    else:
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text=settings.WRONG
        )


@utils.send_typing_action
def file_handler(bot, update):
    """
    Handler of telegram messages with either document or image

    :param bot:
    :param update:
    :return:
    """
    if update.message.document or update.message.photo:
        if update.message.caption and '#bugs' in update.message.caption:

            if update.message.document:
                attach = update.message.document
            else:
                attach = update.message.photo[-1]

            mime_type = getattr(attach, 'mime_type', 'image')
            file_name = getattr(attach, 'file_name', 'noname')
            file = bot.get_file(attach.file_id)
            if update.message.caption:
                bug_text = update.message.caption
            else:
                bug_text = 'Bug from Telegram chat'

            if len(bug_text) > 20:
                card_title = f'{bug_text[:20]}...'
            else:
                card_title = bug_text

            trello_list = utils.get_list(update)
            if trello_list:
                card = trello_list.add_card(card_title, bug_text)
                card.attach(
                    file=file.download_as_bytearray(),
                    mimeType=mime_type,
                    name=file_name
                )

                if card:
                    bot.send_message(
                        chat_id=update.message.chat_id,
                        text=f'A card was successfully created: {card.url}'
                    )
                else:
                    bot.send_message(
                        chat_id=update.message.chat_id,
                        text='Failed to create a card'
                    )


@utils.send_typing_action
def message_handler(bot, update):
    """
    Handler for plain text messages
    :param bot:
    :param update:
    :return:
    """
    bug_text = update.message.text
    card_title = f'{bug_text[:20]}...' if len(bug_text) > 20 else bug_text

    trello_list = utils.get_list(update)
    if trello_list:
        card = trello_list.add_card(card_title, bug_text)
        if card:
            bot.send_message(
                chat_id=update.message.chat_id,
                text=f'A card was successfully created: {card.url}'
            )
        else:
            bot.send_message(
                chat_id=update.message.chat_id,
                text='Failed to create a card'
            )


def main():
    """
    Main program function initiating handlers and bot, starting the bot itself
    :return:
    """
    updater = Updater(
        token=settings.TELEGRAM_TOKEN,
        request_kwargs=REQUEST_KWARGS
    )
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(
        Filters.photo | Filters.document,
        file_handler))
    dispatcher.add_handler(MessageHandler(utils.bugs_filter, message_handler))

    dispatcher.add_handler(CommandHandler('config', config))
    dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
