# Перше завдання

from datetime import datetime

def get_days_from_today(date):
    try:
        input_date = datetime.strptime(date, '%Y-%m-%d')
        current_date = datetime.today()
        diff = current_date - input_date
        return diff.days
    except ValueError:
        return None

print(get_days_from_today("2021-10-09"))

#Друге завдання

import random

def get_numbers_ticket(min_num, max_num, quantity):
    if min_num < 1 or max_num > 1000 or quantity < 1 or quantity > max_num - min_num + 1:
        return []

    numbers_set = set()
    while len(numbers_set) < quantity:
        numbers_set.add(random.randint(min_num, max_num))

    return sorted(list(numbers_set))

lottery_numbers = get_numbers_ticket(1, 49, 6)
print("Your lottery numbers:", lottery_numbers)

# Третє завдання

import re

def normalize_phone(phone_number):
    phone_number = re.sub(r'\D', '', phone_number)
    if not phone_number.startswith('+'):
        phone_number = '+380' + phone_number.lstrip('0')
    else:
        phone_number = '+380' + phone_number[3:].lstrip('0')
    
    return phone_number

raw_numbers = [
    "067\\t123 4567",
    "(095) 234-5678\\n",
    "+380 44 123 4567",
    "380501234567",
    "    +38(050)123-32-34",
    "     0503451234",
    "(050)8889900",
    "38050-111-22-22",
    "38050 111 22 11   ",
]

sanitized_numbers = [normalize_phone(num) for num in raw_numbers]
print("Normalized phone numbers for SMS campaigns:", sanitized_numbers)


# Четверте завдання

from datetime import datetime, timedelta

def get_upcoming_birthdays(users):
    today = datetime.today().date()
    upcoming_birthdays = []

    for user in users:
        birthday = datetime.strptime(user["birthday"], "%Y.%m.%d").date()
        birthday_this_year = birthday.replace(year=today.year)
        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)

        days_until_birthday = (birthday_this_year - today).days
        if 0 <= days_until_birthday <= 7:
            if (today + timedelta(days=days_until_birthday)).weekday() >= 5:
                days_until_birthday += 2
            congrats_date = today + timedelta(days=days_until_birthday)
            upcoming_birthdays.append({"name": user["name"], "congratulation_date": congrats_date.strftime("%Y.%m.%d")})

    return upcoming_birthdays

users = [
    {"name": "John Doe", "birthday": "1985.01.23"},
    {"name": "Jane Smith", "birthday": "1990.01.27"}
]

upcoming_birthdays = get_upcoming_birthdays(users)
print("This week's list of greetings:", upcoming_birthdays)