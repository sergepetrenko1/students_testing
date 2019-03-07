from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters
import logging
from backend import Student, convert_task
from random import choice
from texts import greeting, closing
from hidden import token


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


ANSWER, QUESTION, CHOOSE_TEST = range(3)

STUDENTS = {}


def start(bot, update):
    update.message.reply_text(greeting)
    user = Student(update.message.chat['username'], update.message.chat['first_name'], update.message.chat['id'])
    STUDENTS[str(update.message.chat['id'])] = user
    user.get_tests()
    if len(user.tests.keys()) > 1:
        keyboard = [[InlineKeyboardButton(str(i), callback_data='{}&{}'.format(i, user.user_id)) for i in user.tests.keys()]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('text', reply_markup=reply_markup)
        return CHOOSE_TEST
    else:
        for key in user.tests.keys():
            user.current_test = key
        cur_test = user.current_test

    for key in user.tests[cur_test].keys():
        if user.tests[cur_test][key]:
            task = choice(user.tests[cur_test][key])
            task_text, choices_points = convert_task(key, task)
            user.tests[cur_test][key].remove(task)
            keyboard = [
                [InlineKeyboardButton(i[0], callback_data='{}&{}'.format(i[1], user.user_id)) for i
                 in choices_points]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(task_text, reply_markup=reply_markup)
            return ANSWER

    else:
        update.message.reply_text(closing)
    return ANSWER


def button(bot, update):
    query = update.callback_query
    user_id = query.data.split('&')[1]
    stud = STUDENTS[user_id]
    stud.update_grade(query.data.split('&')[0])
    query.edit_message_text(text="You've got {} points\n Send any text to continue".format(query.data.split('&')[0]))

    return QUESTION


def send_question(bot, update):
    student = STUDENTS[str(update.message.chat['id'])]
    print(student.tests)
    cur_test = student.current_test
    for key in student.tests[cur_test].keys():
        if student.tests[cur_test][key]:
            task = choice(student.tests[cur_test][key])
            task_text, choices_points = convert_task(key, task)
            student.tests[cur_test][key].remove(task)
            keyboard = [
                [InlineKeyboardButton(i[0], callback_data='{}&{}'.format(i[1], student.user_id)) for i
                 in choices_points]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(task_text, reply_markup=reply_markup)
            return ANSWER

    update.message.reply_text(closing)
    student.submit_test()

    return QUESTION


def choose_test(bot, update):
    query = update.callback_query
    user_id = query.data.split('&')[1]
    stud = STUDENTS[user_id]
    stud.current_test = query.data.split('&')[0]
    query.edit_message_text('You have selected {}\nSend any text to begin'.format(stud.current_test))
    return QUESTION


def main():
    updater = Updater(token=token)
    dp = updater.dispatcher
    cv_handler = ConversationHandler(
             per_user=True,
             entry_points=[CommandHandler('start', start)],
             states={

                 CHOOSE_TEST: [CallbackQueryHandler(choose_test)],

                 ANSWER: [CallbackQueryHandler(button)],

                 QUESTION: [MessageHandler(Filters.text, send_question), CommandHandler('start', start)],

             },
             fallbacks=[ConversationHandler.END]
         )

    dp.add_handler(cv_handler)
    updater.start_polling()

    updater.idle()


main()
