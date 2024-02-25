from datetime import date
from dateutil.relativedelta import relativedelta, MO


def get_date():
  today = date.today()
  return today.strftime("%d/%m/%Y")


def get_closest_weekday(weekday):
  return (date.today() + relativedelta(weekday=weekday)).strftime("%d/%m/%Y")
