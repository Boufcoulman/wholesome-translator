import sqlite3
from typing import NamedTuple, List, Optional
from dateutil.parser import parse
import datetime
from lib.load_var import get_var

# https://www.tutorialspoint.com/How-to-store-and-retrieve-date-into-Sqlite3-database-using-Python

# Database stored locally
BIRTHDAY_DB = get_var('BIRTHDAY_DB')
BIRTHDAY_TABLE = get_var('BIRTHDAY_TABLE')

# Months of the year in french
MOIS = {str(number): name for number, name in enumerate([
    'janvier', 'février', 'mars', 'avril', 'mai', 'juin',
    'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'],
    1)}
MOIS_INV = dict(zip(MOIS.values(), MOIS.keys()))


class Birthday(NamedTuple):
    """ A named tuple representing a birthday.

    Attributes:
        user_id: The id of the user whose birthday it is
        birthday: The date of the birthday
    """
    user_id: int
    birthday: str


def init_birthday_db():
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


def update_birthday(user: int, birthday: str):
    """Add or modify the birthday of the wanted user.

    Args:
        user: discord identifier of the user
        birthday: birthday date of the user ('dd-mm')
    """
    conn = sqlite3.connect(BIRTHDAY_DB)
    cursor = conn.cursor()

    # Update birthday for specified user
    cursor.execute(
        f"""INSERT OR REPLACE INTO {BIRTHDAY_TABLE}
        (user, birthday) VALUES (?,?)""",
        (user, birthday),
    )
    conn.commit()
    conn.close()


def remove_birthday(user: str):
    """Remove the birthday of the wanted user.

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


def get_birthdays(date: datetime.date) -> List[int]:
    """Get the users whose birthdays are on date.

    Args:
        date: the date on which we want to know who were born

    Returns:
        the list of users who were born on date, empty if no users were born
    """
    conn = sqlite3.connect(BIRTHDAY_DB)
    cursor = conn.cursor()

    # Get the list of birthdays
    cursor.execute(f"""
    SELECT user FROM {BIRTHDAY_TABLE} WHERE birthday='{db_date(date)}'
    """)
    users = [user_record[0] for user_record in cursor]

    return users


def get_all_birthdays() -> List[Birthday]:
    """Get all the birthdays.

    Returns:
        the list of bithday's tuples
    """
    conn = sqlite3.connect(BIRTHDAY_DB)
    cursor = conn.cursor()

    # Get the list of users
    cursor.execute(f"""
    SELECT user, birthday FROM {BIRTHDAY_TABLE}
    ORDER BY SUBSTR(birthday, 4, 2), SUBSTR(birthday, 1, 2)
    """)
    birthdays = [Birthday(*record) for record in cursor]

    return birthdays


def db_date(date: datetime.date) -> str:
    """Convert date to be stored in the database."""
    return f"{date.day}-{date.month}"


def display_db_date(db_date: str) -> str:
    """Convert db_date to be nicely displayed."""
    day, month = db_date.split('-')
    return f"{day} {MOIS[month]}".title()


def date_parser(date_input: str):
    """Test if input is a valide birthday date.

    Args:
        date_input: the input to be tested as a date

    Returns:
        date as 'day-month' if input is valid, None otherwise

    Usage: date = date_parser('27-05')
    """
    # Month in full letter handling
    date_input = [check_if_month(elem) or elem for elem in date_input]

    try:
        # 1964 is a leap year, so it will allow the 29 of february
        date = parse(' '.join(date_input) + ' 1964',
                     dayfirst=True,
                     yearfirst=False)
        return db_date(date)
    except Exception:
        return None


def check_if_month(month_name: str) -> Optional[str]:
    """Verify if month exists in letter and return associated number.

    Args:
        month_name: the name to test as a month

    Returns:
        the month number if the name is valid, None otherwise
    """
    return MOIS_INV.get(month_name.lower())


if __name__ == '__main__':
    init_birthday_db()

    print(display_db_date('1-12'))
    # update_birthday(1, date_parser("16-04"))
    # update_birthday(2, date_parser("13-04"))
    # update_birthday(12, date_parser("13-04"))
    # update_birthday(75240, date_parser("25-04"))
    # remove_birthday(75240)
    print(get_birthdays('13-4'))
    print(get_all_birthdays())
    print(date_parser('0-05'))
    print(parse('65 5', dayfirst=True, yearfirst=False))
    print(datetime.date.today())
    print('oui'
          if date_parser('25-7') == db_date(datetime.date.today())
          else None)
