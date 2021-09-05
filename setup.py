from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.update import Update
from telegram.error import TelegramError
from EgyRequest.Request import get_shows, get_info, get_links, get_season, get_episode
from EgyFucntions.Function import inline
from EgyRequest.Text import command_prevent_message, all_prevent_message, select_type_message
from pprint import pprint
import logging
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Handler,
    Filters,
    CallbackQueryHandler,
    ConversationHandler,
)

# State definitions for conversation
(
    TYPING,
    SELECTING_SHOW,
    SELECTING_TYPE,
    SELECTING_QUALITY,
    SELECTING_SEASON,
    SELECTING_EPISODE,
    PREVENT_COMMAND,
    PREVENT_ALL,
    BRANCH,

 ) = map(str,range(0,9))

# Shortcut for ConversationHandler.END
END = ConversationHandler.END
TIMEOUT = ConversationHandler.TIMEOUT

logging.basicConfig(format='|(%(asctime)s)| - |%(name)s| - |%(levelname)s| => %(message)s', level=logging.INFO)
logger = logging.getLogger('Hesham')

# api_id = 7674707
# api_hash = '165eb092814f4a54e215e0c03b844de7'

channel_id = -1001591746087

def start(update, context):
    '''Getting input from user, then search it'''
    try:
        member = context.bot.getChatMember(chat_id=channel_id, user_id=update.message.chat_id)
        if member.status == 'left':
            raise TelegramError(message='the member not in group')
    except:
        update.message.reply_text(text='الرجاء الاشتراك في القناة اولا، @Egybot_Community')
        return END
    else:
        update.message.reply_text(text='الرجاء كتابة فيلمك المفضل')
        return SELECTING_SHOW

def input_search(update, context):
    '''Handling inputs received from user'''

    # send the user input fo searching
    if context.user_data.get('shows'):
        shows = context.user_data['shows']
    else:
        shows = get_shows(update.message.text)

    if shows:
        # getting shows photos and name.
        photos = shows['display']['imgs']

        # sending shows and inline keyboard reply
        buttons = shows['display']['buttons']
        buttons_markup = InlineKeyboardMarkup(buttons)

        if context.user_data.get('shows'):
            update.callback_query.edit_message_text(text='نرجو من اختيار احد الأفلام القادمة مع مراعة اختياراتها بشكل صحيح وشكرا لكم جداا:', reply_markup=buttons_markup)
        else:
            context.bot.send_media_group(chat_id=update.message.chat_id, media=photos)
            update.message.reply_text(text='نرجو من اختيار احد الأفلام القادمة مع مراعة اختياراتها بشكل صحيح وشكرا لكم جداا:', reply_markup=buttons_markup)

        # saving shows to the user data for next steps
        context.user_data['shows'] = shows

        return SELECTING_TYPE

    else:
        update.message.reply_text(text='لا يوجد نتائج، الرجاء المحاولة مرة اخرى')


def command_prevent(update, context):
    context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
    update.message.reply_text(text=command_prevent_message)

def all_prevent(update, context):
    context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
    update.message.reply_text(text=all_prevent_message)

def select_type(update, context):
    if not context.user_data.get('selected_show'):
        selected_show = context.user_data['shows'][update.callback_query.data]
        context.user_data['selected_show'] = selected_show
    else:
        selected_show = context.user_data['selected_show']

    if not context.user_data.get('selected_show_attrs'):
        update.callback_query.edit_message_text(text='الرجاء الإنتظار لبضع ثواني', parse_mode=ParseMode.MARKDOWN)
        info = get_info(selected_show)
        context.user_data['selected_show_attrs'] = info
    else:
        info = context.user_data['selected_show_attrs']

    buttons = [
        [InlineKeyboardButton(text='تحميل', callback_data='dl'),
        InlineKeyboardButton(text='مشاهدة', callback_data='watch')],
        [InlineKeyboardButton(text='الرجوع لقائمة العرض', callback_data='back_shows')]
    ]
    buttons_markup = InlineKeyboardMarkup(buttons)

    update.callback_query.edit_message_text(text=select_type_message(info), reply_markup=buttons_markup)

    if selected_show['type'] == 'movie':
        print('movie33')
        return SELECTING_QUALITY
    else:
        print('series33')
        return SELECTING_SEASON

def select_season(update, context):
    print('season')
    print(update.callback_query.data)
    info = context.user_data['selected_show_attrs']
    selected_show = context.user_data['selected_show']
    update.callback_query.edit_message_text(text='من فضلك انتظر قليلا', parse_mode=ParseMode.MARKDOWN)

    seasons = get_season(selected_show['url'])

    back_show_button = [[InlineKeyboardButton(text='الرجوع للخلف', callback_data='back_to_type_season')],
                        [InlineKeyboardButton(text='الرجوع لقائمة العرض', callback_data='back_shows')]
                        ]
    buttons = inline([InlineKeyboardButton(text=f'الموسم - {i+1}', callback_data=i) for i in range(len(seasons))], add=back_show_button)

    # edit the message and reply markup
    buttons_markup = InlineKeyboardMarkup(buttons)
    update.callback_query.edit_message_text(text=select_type_message(info), reply_markup=buttons_markup)

    context.user_data['seasons'] = seasons

    if not context.user_data.get('watch_type'):
        context.user_data['watch_type'] = update.callback_query.data

    return SELECTING_EPISODE

def select_episode(update, context):
    update.callback_query.edit_message_text(text='من فضلك انتظر قليلا', parse_mode=ParseMode.MARKDOWN)

    info = context.user_data['selected_show_attrs']
    season = context.user_data['seasons']

    if not context.user_data.get('selected_season'):
        episode_url = season[int(update.callback_query.data)]
        context.user_data['selected_season'] = episode_url
    else:
        episode_url = context.user_data['selected_season']

    episodes = get_episode(episode_url)

    back_show_button = [[InlineKeyboardButton(text='الرجوع للخلف', callback_data='back_season')],
                        [InlineKeyboardButton(text='الرجوع لقائمة العرض', callback_data='back_shows')]
                        ]
    buttons = inline([InlineKeyboardButton(text=f'الحلقة - {i + 1}', callback_data=i) for i in range(0, len(episodes))],
                     add=back_show_button)

    # edit the message and reply markup
    buttons_markup = InlineKeyboardMarkup(buttons)
    update.callback_query.edit_message_text(text=select_type_message(info), reply_markup=buttons_markup)

    context.user_data['episodes'] = episodes

    return SELECTING_QUALITY

def select_quality(update, context):
    print('quality')
    print(update.callback_query.data)
    info = context.user_data['selected_show_attrs']
    selected_show = context.user_data['selected_show']

    if selected_show['type'] == 'movie':
        print('movie')
        selected_url = selected_show['url']
        type = update.callback_query.data
        back_show_button = [[InlineKeyboardButton(text='الرجوع للخلف', callback_data='back_to_type_quality')], [InlineKeyboardButton(text='الرجوع لقائمة العرض', callback_data='back_shows')]]
    else:

        if not context.user_data.get('selected_episode'):
            selected_url = context.user_data['episodes'][int(update.callback_query.data)]
        else:
            selected_url = context.user_data['selected_episode']

        type = context.user_data['watch_type']
        back_show_button = [[InlineKeyboardButton(text='الرجوع للخلف', callback_data='back_episode')], [InlineKeyboardButton(text='الرجوع لقائمة العرض', callback_data='back_shows')]]

    update.callback_query.edit_message_text(text='الرجاء الإنتظار لمدة اقصاها 5 ثواني', parse_mode=ParseMode.MARKDOWN)

    links = get_links(selected_url, type=type)

    # check if movie is available
    if not links['links']:
        update.callback_query.answer(text='للأسف الفيلم أو المسلسل الذي اخترته غير متاح للمشاهدة أو التحميل', show_alert=True)
        buttons = [[InlineKeyboardButton(text='الرجوع للخلف', callback_data='back_shows')]]
    else:
        links_table = links['links_table']
        buttons = inline([InlineKeyboardButton(text=f'{links_table[i]} - {links_table[i+1]}', callback_data=f'{links_table[i]}', url=links['links'][int(i/2)]) for i in range(0, len(links_table), 2)], add=back_show_button)

    # edit the message and reply markup
    buttons_markup = InlineKeyboardMarkup(buttons)
    update.callback_query.edit_message_text(text=select_type_message(info), reply_markup=buttons_markup)

    if context.user_data['selected_show']['type'] == 'series':
        context.user_data['selected_episode'] = context.user_data['episodes'][int(update.callback_query.data)]


def back_to_shows(update, context):
    print('back_to_shows')
    del context.user_data['selected_show']
    del context.user_data['selected_show_attrs']
    input_search(update, context)

    return SELECTING_TYPE

def back_to_type_quality(update, context):
    print('back_to_type_quality')
    select_type(update, context)

    return SELECTING_QUALITY

def back_to_type_season(update, context):
    print('back_to_type_season')
    del context.user_data['seasons']
    del context.user_data['watch_type']
    select_type(update, context)

    return SELECTING_SEASON

def back_to_season(update, context):
    print('back_to_season')
    del context.user_data['selected_season']
    del context.user_data['episodes']
    select_season(update, context)

    return SELECTING_EPISODE

def back_to_episode(update, context):
    print('back_to_episode')
    del context.user_data['selected_episode']
    select_episode(update, context)

    return SELECTING_QUALITY

def timeout(update, context):
    print('timeout')
    context.user_data.clear()
    if not update.callback_query:
        context.bot.send_message(chat_id=update.message.chat_id, text='انتهى الوقت.')
    else:
        context.bot.send_message(chat_id=update.callback_query.message.chat_id, text='انتهى الوقت.')

    return TIMEOUT

def cancel(update, context):
    print('cancel')
    context.user_data.clear()
    
    return END

def error(update, context):
    print('error')
    logging.warning(msg=context.error)

def others(update, context):
    print('others')


def main():
    '''This Function Initiate The Bot '''

    Token = '1979999444:AAGuFJiCYCtVB7m2jQojH8zbuYh4F_lU2_o'
    updater = Updater(token=Token)
    dispatcher = updater.dispatcher

    # inline_conversation_handler = ConversationHandler(
    #     entry_points=[, MessageHandler(Filters.text &(~Filters.regex(f'^/cancel$')), all_prevent)],
    #     states={
    #     },
    #     fallbacks=[MessageHandler(Filters.text &(~Filters.regex(f'^/cancel$')), all_prevent),
    #                CallbackQueryHandler(back_to_shows, pattern=f'^back_shows$', run_async=True),
    #                CallbackQueryHandler(back_to_type, pattern=f'^back_type$', run_async=True),
    #                CommandHandler('cancel', cancel)
    #     ],
    #     map_to_parent={
    #         SELECTING_TYPE: SELECTING_TYPE,
    #         END: END,
    #     }
    #

    search_conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SELECTING_SHOW: [MessageHandler(Filters.text & (~Filters.command), input_search)],
            SELECTING_TYPE: [CallbackQueryHandler(select_type, pattern='\d+')],
            SELECTING_SEASON: [CallbackQueryHandler(select_season, pattern=f'^(watch|dl)$')],
            SELECTING_EPISODE: [CallbackQueryHandler(select_episode, pattern=f'\d+')],
            SELECTING_QUALITY: [CallbackQueryHandler(select_quality, pattern=f'^(watch|dl|\d+)$')],
            ConversationHandler.TIMEOUT: [MessageHandler(Filters.all, timeout), CallbackQueryHandler(timeout)]
        },
        fallbacks=[MessageHandler(Filters.text &(~Filters.regex(f'^/cancel$')), all_prevent),
                   CallbackQueryHandler(back_to_shows, pattern=f'^back_shows$'),
                   CallbackQueryHandler(back_to_type_quality, pattern=f'^back_to_type_quality'),
                   CallbackQueryHandler(back_to_type_season, pattern=f'^back_to_type_season'),
                   CallbackQueryHandler(back_to_season, pattern=f'^back_season$'),
                   CallbackQueryHandler(back_to_episode, pattern=f'^back_episode$'),
                   CallbackQueryHandler(others),
                   CommandHandler('cancel', cancel)],
        run_async=True,
        conversation_timeout=10
    )

    dispatcher.add_handler(search_conversation_handler)
    # dispatcher.add_handler(member_handler)

    updater.start_polling()
    updater.idle()

main()
