from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.error import TelegramError
from EgyRequest.Request import get_shows, get_info, get_links, get_season, get_episode
from EgyFucntions.Function import inline
from EgyRequest.Text import command_prevent_message, select_type_message, quality_wait_message, timeout_message, cancel_message, sleep_message, help_message, cancel_nothing_message
import logging
import asyncio
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
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

special_dict = {
    'watch': 'مشاهدة',
    'dl': 'تحميل',
}

channel_id = -1001591746087

async def browser_quit(broswer):

    return broswer.quit()

def bot_stiker_set(sticker, update, context):
    called_sticker = {
        'done':2,
        'sleep':5,
        'up':6,
        'think':7,
        'error': 10,
    }
    sticker_set = context.bot.get_sticker_set(name="RoboCatBot")
    context.bot.send_sticker(chat_id=update.effective_chat.id, sticker=sticker_set.stickers[called_sticker[sticker]])

def start(update, context):
    '''Getting input from user, then search it'''
    try:
        member = context.bot.getChatMember(chat_id=channel_id, user_id=update.message.chat_id)
        if member.status == 'left':
            raise TelegramError(message='the member not in group')
    except:
        update.message.reply_text(text='الرجاء الاشتراك في القناة اولا، @Egybot_Community')
        bot_stiker_set('up', update, context)
        return END
    else:
        update.message.reply_text(text='الرجاء كتابة الفيلم أو المسلسل الذي تريد البحث عنه:', reply_to_message_id=update.message.message_id)
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
            update.callback_query.edit_message_text(text='يمكنك الآن الإختيار من هذه القوائم (يمكنك الرجوع إليها لاحقًا):', reply_markup=buttons_markup)
        else:
            try:
                context.bot.send_media_group(chat_id=update.message.chat_id, media=photos, reply_to_message_id=update.message.message_id)
            except:
                update.message.reply_text(text='لقد حدثت مشكلة أثناء تحميل الصو، ولكن لحسن الحظ يمكنك الإستمرار في إختيار فيلمك أو مسلسلك')
            update.message.reply_text(text='يمكنك الآن الإختيار من هذه القوائم (يمكنك الرجوع إليها لاحقًا):', reply_markup=buttons_markup)

        # saving shows to the user data for next steps
        context.user_data['shows'] = shows

        return SELECTING_TYPE

    else:
        update.message.reply_text(text='لا يوجد نتائج، الرجاء كتابة الفيلم أو المسلسل الذي تريد البحث عنه مرة أخرى:')


def all_prevent(update, context):
    bot_stiker_set('error', update, context)
    context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
    update.message.reply_text(text=command_prevent_message, parse_mode=ParseMode.MARKDOWN)

def select_type(update, context):
    if not context.user_data.get('selected_show'):
        selected_show = context.user_data['shows'][update.callback_query.data]
        context.user_data['selected_show'] = selected_show
    else:
        selected_show = context.user_data['selected_show']

    if not context.user_data.get('selected_show_attrs'):
        update.callback_query.edit_message_text(text='الرجاء الإنتظار قليلًا', parse_mode=ParseMode.MARKDOWN)
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

    update.callback_query.edit_message_text(text=select_type_message(info), reply_markup=buttons_markup, parse_mode=ParseMode.MARKDOWN)

    if selected_show['type'] == 'movie':
        return SELECTING_QUALITY
    else:
        return SELECTING_SEASON

def select_season(update, context):
    info = context.user_data['selected_show_attrs']
    selected_show = context.user_data['selected_show']
    update.callback_query.edit_message_text(text='الرجاء الإنتظار قليلًا', parse_mode=ParseMode.MARKDOWN)

    seasons = get_season(selected_show['url'])

    back_show_button = [[InlineKeyboardButton(text='الرجوع للخلف', callback_data='back_to_type_season')],
                        [InlineKeyboardButton(text='الرجوع لقائمة العرض', callback_data='back_shows')]
                        ]
    buttons = inline([InlineKeyboardButton(text=f'الموسم - {i+1}', callback_data=i) for i in range(len(seasons))], add=back_show_button)
    # edit the message and reply markup
    buttons_markup = InlineKeyboardMarkup(buttons)
    type_appear = context.user_data['watch_type'] if context.user_data.get('watch_type') else update.callback_query.data
    update.callback_query.edit_message_text(text=select_type_message(info, [special_dict[type_appear]]), reply_markup=buttons_markup, parse_mode=ParseMode.MARKDOWN)

    context.user_data['seasons'] = seasons

    if not context.user_data.get('watch_type'):
        context.user_data['watch_type'] = update.callback_query.data

    return SELECTING_EPISODE

def select_episode(update, context):
    update.callback_query.edit_message_text(text='الرجاء الإنتظار قليلًا', parse_mode=ParseMode.MARKDOWN)

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
    season_appear = season.index(context.user_data['selected_season']) if context.user_data.get('selected_season') else update.callback_query.data
    update.callback_query.edit_message_text(text=select_type_message(info, add=[special_dict[context.user_data['watch_type']],f'الموسم  {int(season_appear) + 1}']), reply_markup=buttons_markup, parse_mode=ParseMode.MARKDOWN)

    context.user_data['episodes'] = episodes

    return SELECTING_QUALITY

def select_quality(update, context):
    info = context.user_data['selected_show_attrs']
    selected_show = context.user_data['selected_show']

    if selected_show['type'] == 'movie':
        selected_url = selected_show['url']
        type = update.callback_query.data
        back_show_button = [[InlineKeyboardButton(text='الرجوع للخلف', callback_data='back_to_type_quality')], [InlineKeyboardButton(text='الرجوع لقائمة العرض', callback_data='back_shows')]]
        type_appear = context.user_data['watch_type'] if context.user_data.get('watch_type') else update.callback_query.data
        add = [special_dict[type_appear]]
    else:
        season = context.user_data['seasons']
        episodes = context.user_data['episodes']
        if not context.user_data.get('selected_episode'):
            selected_url = episodes[int(update.callback_query.data)]
        else:
            selected_url = context.user_data['selected_episode']

        type = context.user_data['watch_type']
        back_show_button = [[InlineKeyboardButton(text='الرجوع للخلف', callback_data='back_episode')], [InlineKeyboardButton(text='الرجوع لقائمة العرض', callback_data='back_shows')]]
        episode_appear = episodes.index(context.user_data['selected_episode']) if context.user_data.get('selected_episode') else update.callback_query.data
        add = [special_dict[context.user_data['watch_type']], f'الموسم  {int(season.index(context.user_data["selected_season"])) + 1}', f'الحلقة  {int(episode_appear) + 1}']

    update.callback_query.edit_message_text(text=quality_wait_message, parse_mode=ParseMode.MARKDOWN)

    links, browser = get_links(selected_url, type=type)

    # check if movie is available
    if not links:
        update.callback_query.answer(text='للأسف الفيلم أو المسلسل الذي اخترته غير متاح للمشاهدة أو التحميل', show_alert=True)
        buttons = [[InlineKeyboardButton(text='الرجوع للخلف', callback_data='back_shows')]]
        update.callback_query.edit_message_text(text=select_type_message(info, add=add, links=links), parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(buttons))

    else:
        links_table = links['links_table']
        update.callback_query.edit_message_text(text=select_type_message(info, add=add, links=links), parse_mode=ParseMode.MARKDOWN)
        # edit the message and reply markup
        # buttons_inline = [InlineKeyboardButton(text=f'{links_table[i]} - {links_table[i+1]}', callback_data=f'{links_table[i]}', url=links['links'][int(i/2)]) for i in range(0, len(links_table), 2)]
        # buttons = inline(buttons_inline)

    if context.user_data['selected_show']['type'] == 'series':
        context.user_data['selected_episode'] = context.user_data['episodes'][int(update.callback_query.data)]

    if links:
        browser.quit()
        print('quit')
        update.callback_query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(back_show_button))

def back_to_shows(update, context):
    del context.user_data['selected_show']
    del context.user_data['selected_show_attrs']
    input_search(update, context)

    return SELECTING_TYPE

def back_to_type_quality(update, context):
    select_type(update, context)

    return SELECTING_QUALITY

def back_to_type_season(update, context):
    del context.user_data['seasons']
    del context.user_data['watch_type']
    select_type(update, context)

    return SELECTING_SEASON

def back_to_season(update, context):
    del context.user_data['selected_season']
    del context.user_data['episodes']
    select_season(update, context)

    return SELECTING_EPISODE

def back_to_episode(update, context):
    del context.user_data['selected_episode']
    select_episode(update, context)

    return SELECTING_QUALITY

def timeout(update, context):
    context.user_data.clear()
    if not update.callback_query:
        context.bot.send_message(chat_id=update.message.chat_id, text=timeout_message, parse_mode=ParseMode.MARKDOWN)
    else:
        context.bot.send_message(chat_id=update.callback_query.message.chat_id, text=timeout_message, parse_mode=ParseMode.MARKDOWN)

    return TIMEOUT

def cancel(update, context):
    context.user_data.clear()
    bot_stiker_set('done', update, context)
    update.message.reply_text(text=cancel_message, parse_mode=ParseMode.MARKDOWN)
    
    return END

def error(update, context):
    logging.warning(msg=context.error)

def prevent_common_message(update, context):
    bot_stiker_set('think', update, context)
    update.message.reply_text(text=sleep_message, parse_mode=ParseMode.MARKDOWN)

def help_handle(update, context):
    update.message.reply_text(text=help_message)

def cancel_nothing(update, context):
    bot_stiker_set('sleep', update, context)
    update.message.reply_text(text=cancel_nothing_message, parse_mode=ParseMode.MARKDOWN)

def main():
    '''This Function Initiate The Bot '''

    Token = '1979999444:AAGuFJiCYCtVB7m2jQojH8zbuYh4F_lU2_o'
    updater = Updater(token=Token)
    dispatcher = updater.dispatcher

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
                   CommandHandler('cancel', cancel)],
        run_async=True,
        conversation_timeout=60*60*3
    )

    dispatcher.add_handler(search_conversation_handler, group=0)
    dispatcher.add_handler(CommandHandler('help', help_handle))
    dispatcher.add_handler(CommandHandler('cancel', cancel_nothing))

    updater.start_polling()
    updater.idle()

main()
