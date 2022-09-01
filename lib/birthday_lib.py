"""Functions to manage the birthday functionalities in the database."""

import datetime
import sqlite3
from typing import NamedTuple

from dateutil.parser import ParserError
from dateutil.parser import parse as parse_date

from lib.load_var import get_var

# https://www.tutorialspoint.com/How-to-store-and-retrieve-date-into-Sqlite3-database-using-Python

# Database stored locally
BIRTHDAY_DB = get_var('BIRTHDAY_DB')
BIRTHDAY_TABLE = get_var('BIRTHDAY_TABLE')

MONTHS = (
    'janvier',
    'février',
    'mars',
    'avril',
    'mai',
    'juin',
    'juillet',
    'août',
    'septembre',
    'octobre',
    'novembre',
    'décembre',
)


def get_month(number: int) -> str | None:
    """Get the name of the month from its number.

    Args:
        number: the number of the month

    Returns:
        the name of the month in lowercase French or None
        if the number is not correct

    >>> get_month(2)
    'février'
    >>> get_month(14)
    """
    try:
        return MONTHS[number - 1]
    except IndexError:
        return None


def get_month_number(month: str) -> int | None:
    """Get the number of the month from its French name.

    Args:
        month: the name of the month in French

    Returns:
        the number of the month starting with 1 for January
        or None if the name is incorrect

    >>> get_month_number('FéVriEr')
    2

    >>> get_month_number('')
    >>> get_month_number('may')
    """
    try:
        return MONTHS.index(month.lower()) + 1
    except ValueError:
        return None


class Birthday(NamedTuple):
    """A named tuple representing a birthday.

    Attributes:
        user_id: The id of the user whose birthday it is
        birthday: The date of the birthday
    """

    user_id: int
    birthday: str


def init_birthday_db() -> None:
    """Initialize the database meant to gather birthday dates."""
    conn = sqlite3.connect(BIRTHDAY_DB)
    cursor = conn.cursor()

    # Create birthday table if not existing
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {BIRTHDAY_TABLE} (
        user INTEGER PRIMARY KEY,
        birthday TEXT
    )
    """)


def update_birthday(user: int, birthday: str) -> None:
    """Add or modify the birthday of the wanted user.

    Args:
        user: discord identifier of the user
        birthday: birthday date of the user ('dd-mm')
    """
    conn = sqlite3.connect(BIRTHDAY_DB)
    cursor = conn.cursor()

    # Update birthday for specified user
    request = f"""INSERT OR REPLACE INTO {BIRTHDAY_TABLE}
                  (user, birthday) VALUES (?,?)"""
    cursor.execute(request, (user, birthday))
    conn.commit()
    conn.close()


def remove_birthday(user: int) -> None:
    """Remove the birthday of the wanted user.

    Args:
        user: discord identifier of the user
    """
    conn = sqlite3.connect(BIRTHDAY_DB)
    cursor = conn.cursor()

    # Delete birthday for specified user
    request = f"""
    DELETE FROM {BIRTHDAY_TABLE} WHERE user=?
    """
    cursor.execute(request, (user,))
    conn.commit()
    conn.close()


def get_birthdays(date: datetime.date) -> list[int]:
    """Get the users whose birthdays are on given date.

    Args:
        date: the date on which we want to know who were born

    Returns:
        the list of users who were born on date, empty if no users were born
    """
    conn = sqlite3.connect(BIRTHDAY_DB)
    cursor = conn.cursor()

    # Get the list of birthdays
    request = f"""
        SELECT user FROM {BIRTHDAY_TABLE} WHERE birthday=?
    """
    cursor.execute(request, (db_date(date),))

    return [user_record[0] for user_record in cursor]


def get_all_birthdays() -> list[Birthday]:
    """Get all the birthdays.

    Returns:
        the list of bithday's tuples
    """
    conn = sqlite3.connect(BIRTHDAY_DB)
    cursor = conn.cursor()

    # Get the list of users
    cursor.execute(f"""
    SELECT user, birthday FROM {BIRTHDAY_TABLE}
    ORDER BY birthday
    """)

    return [Birthday(*record) for record in cursor]


def db_date(date: datetime.date) -> str:
    """Convert date to be stored in the database.

    Args:
        date: the date to convert to string

    Returns:
        the date converted to the format used in the database

    >>> db_date(datetime.date.fromisoformat('2022-01-01'))
    '2022-01-01'
    """
    return date.isoformat()


def display_db_date(date_db: str) -> str:
    """Convert db_date to be nicely displayed.

    Args:
        date_db: the date in the database format

    Returns:
        the date formated in a user readable form

    >>> display_db_date('1964-02-29')
    '29 Février'
    """
    _, month, day = date_db.split('-')
    month_name = get_month(int(month))

    return f'{day} {month_name}'.title()


def date_parser(date_input: str) -> str | None:
    """Test if input is a valid birthday date.

    Args:
        date_input: the input to be tested as a date

    Returns:
        date as 'day-month' if input is valid, None otherwise

    >>> date_parser('27-05')
    '1964-05-27'
    >>> date_parser('27 05')
    '1964-05-27'
    >>> date_parser('27-mai')
    '1964-05-27'
    >>> date_parser('27 mai')
    '1964-05-27'
    >>> date_parser('   27      05  ')
    '1964-05-27'
    >>> date_parser('')
    """
    if not date_input:
        return None

    # 1964 is a leap year, so it will allow the 29 of february
    date_input = f'{date_input}-1964'
    date_input = date_input.replace('-', ' ').split(' ')
    # Month in full letter handling
    date_input = [str(get_month_number(elem) or elem) for elem in date_input]
    try:
        date = parse_date(' '.join(date_input), dayfirst=True, yearfirst=False)
    except (ParserError, OverflowError):
        return None
    return db_date(date.date())
