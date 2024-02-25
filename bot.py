#!/usr/bin/python3

import os
import auth
import logging
from dates import get_closest_weekday
from dates import get_date
from main import search_available
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes,
    CallbackQueryHandler, ConversationHandler, MessageHandler, filters
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

START, AWAITING_MESSAGE = range(2)


def main_menu_message():
  return 'Choose the day:'


def main_menu_keyboard():
  weekdays = ["Monday", "Tuesday", "Wednesday",
              "Thursday", "Friday", "Saturday", "Sunday"]
  keyboard = [InlineKeyboardButton(
      weekdays[i], callback_data=i) for i in range(7)]
  return InlineKeyboardMarkup.from_column(keyboard)


async def start(bot, update):
  # await bot.message.reply_text("dfafas")
  await bot.message.reply_text(main_menu_message(),
                               reply_markup=main_menu_keyboard())
  return AWAITING_MESSAGE


async def push_messages(f, res):
  if res:
    for x in res:
      await f(x)
  else:
    await f("No results for this selection !")


async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  """Parses the CallbackQuery and updates the message text."""
  query = update.callback_query
  await query.answer()
  date = get_closest_weekday(int(query.data))

  context.user_data['date'] = date
  await update.effective_message.reply_text("Choose arrondissements seperated with spaces, input 0 for all:")
  # msg = update.effective_message.text


async def handle_message(update: Update, context):
  print("HANDLE", flush=True)
  message = update.message.text
  arronds = message.split(" ")
  if not (all(map(str.isnumeric, arronds))):
    await update.message.reply_text(f"All numbers should be numeric values !")
    return AWAITING_MESSAGE
  arronds = list(map(int, arronds))
  if not list(filter(lambda a: a in range(1, 21), arronds)):
    arronds = list(range(1, 21))
  config = {
      'date': context.user_data['date'],
      'hours': '10-20',
      'couvert': True,
      'arronds': arronds
  }
  print(config)
  res = search_available(config)
  await push_messages(update.message.reply_text, res)
  return AWAITING_MESSAGE


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  await update.message.reply_text(f'Hello {update.effective_user.first_name}')


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  date = get_date()
  if len(context.args) > 0:
    date = context.args[0]
  print(date)
  if len(context.args) > 1:
    arronds = list(map(int, context.args[1:]))
  else:
    arronds = list(range(1, 21))
  config = {
      'date': date,
      'hours': '10-20',
      'couvert': True,
      'arronds': arronds
  }
  res = search_available(config)
  # print(res)
  if res:
    for x in res:
      await update.message.reply_text(x)
  else:
    await update.message.reply_text("Pas de résultat !")


async def cancel(update, context):
  await update.message.reply_text("Conversation cancelled.")
  return ConversationHandler.END


def main():
  token = auth.token
  if os.getenv('BOT_TOKEN'):
    token = os.getenv('BOT_TOKEN')

  app = ApplicationBuilder().token(token).build()

  conv_handler = ConversationHandler(
      entry_points=[CommandHandler('start', start)],
      states={
          AWAITING_MESSAGE: [MessageHandler(filters.TEXT, handle_message)]
      },
      fallbacks=[CommandHandler('cancel', cancel)],

  )

  # app.add_handler(CommandHandler("start", start))
  app.add_handler(CommandHandler("hello", hello))
  app.add_handler(CommandHandler("search", search))

  app.add_handler(CallbackQueryHandler(handle_menu))

  app.add_handler(conv_handler)

  app.run_polling()


if __name__ == '__main__':
  main()
