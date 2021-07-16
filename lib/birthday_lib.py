import sqlite3
from typing import NamedTuple
from dateutil.parser import parse
import datetime

# https://www.tutorialspoint.com/How-to-store-and-retrieve-date-into-Sqlite3-database-using-Python

# Database stored locally
BIRTHDAY_DB = 'birthday.db'
BIRTHDAY_TABLE = 'birthday_table'

# Months of the year in french
MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin',
        'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'
        ]


class Birthday(NamedTuple):
    """ A named tuple representing a birthday:

    Attributes:
        user: The user whose birthday it is
        birthday: The date of the birthday
    """
    user: str
    birthday: str


def init_birthday_db():
    """ Initialize the database meant to gather birthday dates
    """
    conn = sqlite3.connect(BIRTHDAY_DB)
    cursor = conn.cursor()

    # Create birthday table if not existing
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {BIRTHDAY_TABLE}(
        user TEXT PRIMARY KEY,
        birthday STRING
    )
    """)


def update_birthday(user: str, birthday: str):
    """Add or modify the birthday of the wanted user

    Args:
        user: discord identifier of the user
        birthday: birthday date of the user
    """
    conn = sqlite3.connect(BIRTHDAY_DB)
    cursor = conn.cursor()

    # Update birthday for specified user
    cursor.execute(f"""
    INSERT OR REPLACE INTO {BIRTHDAY_TABLE}(
        user,
        birthday
        ) VALUES(?,?)""",
                   (user, birthday)
                   )
    conn.commit()
    conn.close()


def remove_birthday(user: str):
    """Remove the birthday of the wanted user

    Args:
        usr: discord identifier of the user
    """
    conn = sqlite3.connect(BIRTHDAY_DB)
    cursor = conn.cursor()

    # Delete birthday for specified user
    cursor.execute(f"""
    DELETE FROM {BIRTHDAY_TABLE} WHERE user='{user}'
    """)
    conn.commit()
    conn.close()


def get_birthdays(date: str) -> [str]:
    """Get the users whose birthdays are on date

    Args:
        date: the date on which we want to know who were born

    Returns:
        the list of users who were born on date, empty if no users were born
    """
    conn = sqlite3.connect(BIRTHDAY_DB)
    cursor = conn.cursor()

    # Get the list of birthdays
    cursor.execute(f"""
    SELECT user FROM {BIRTHDAY_TABLE} WHERE birthday='{date}'
    """)
    users = [user_record[0] for user_record in cursor.fetchall()]

    return users


def get_all_birthdays() -> [Birthday]:
    """Get all the birthdays

    Returns:
        the list of bithday's tuples
    """
    conn = sqlite3.connect(BIRTHDAY_DB)
    cursor = conn.cursor()

    # Get the list of users
    cursor.execute(f"""
    SELECT * FROM {BIRTHDAY_TABLE}
    """)
    birthdays = [
        Birthday(record[0], record[1]) for record in cursor.fetchall()
    ]

    return birthdays


def date_parser(date_input):
    """Test if input is a valide birthday date

    Args:
        date_input: the input to be tested as a date

    Returns:
        the date object if input is valide, None otherwise
    """

    # Month in full letter handling
    date_input = [str(check_if_month(elem)) if check_if_month(elem) else elem
                  for elem in date_input]

    try:
        date = parse(' '.join(date_input), dayfirst=True, yearfirst=False)
        return date
    except Exception:
        return None


def check_if_month(month_name):
    """Verify if month exists in letter and return associated number

    Args:
        month_name: the name to test as a month

    Returns:
        the month number if the name is valid, None otherwise
    """

    month_name = month_name.lower()
    if month_name in MOIS:
        month = MOIS.index(month_name) + 1
        return month
    else:
        return None


if __name__ == "__main__":

    init_birthday_db()
    # update_birthday('yes', datetime.date(2018, 1, 4))
    update_birthday('nouveau', '0504')
    update_birthday('oui#jamie', '0504')
    update_birthday('ousi#jamie', '0504')
    update_birthday('oud#jamie', '0504')
    # remove_birthday('nouveau')
    print(get_birthdays('0504'))
    print(get_all_birthdays())
