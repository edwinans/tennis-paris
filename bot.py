#!/usr/bin/python3

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, Updater
from main import search_available
from auth import token


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  await update.message.reply_text(f'Hello {update.effective_user.first_name}')


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  print(context.args, flush=True)
  date = context.args[0]
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
  print(res)
  if res:
    for x in res:
      await update.message.reply_text(x)
  else:
    await update.message.reply_text("Pas de résultat !")


def main():

  app = ApplicationBuilder().token(token).build()

  app.add_handler(CommandHandler("hello", hello))
  app.add_handler(CommandHandler("search", search))

  app.run_polling()


if __name__ == '__main__':
  main()
