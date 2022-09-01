"""Functions to manage the birthday functionalities in the database."""

import datetime
import logging
import sqlite3
from contextlib import AbstractContextManager
from typing import Any, Callable, NamedTuple

from dateutil.parser import ParserError
from dateutil.parser import parse as parse_date

log = logging.getLogger(__name__)

# https://www.tutorialspoint.com/How-to-store-and-retrieve-date-into-Sqlite3-database-using-Python

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

    def format(self, get_name: Callable[[int], str]) -> str:
        """Format the birthday into a redable form.

        Args:
            get_name: a function that gives a readable name from an ID

        Returns:
            the formatted name
        """
        user = get_name(self.user_id)
        date = display_db_date(self.birthday)
        return f'{user} : {date}'


class DbContextManager(AbstractContextManager[Any]):
    """Generic context manager for a sqlite3 connection."""

    def __init__(self, database: str):
        """Set the database path.

        Args:
            database: path to the database
        """
        self.database = database
        self.conn: sqlite3.Connection | None = None

    def __enter__(self) -> Any:
        """Initialize the connection.

        Returns:
            the DateDb object with an open connection
        """
        self.conn = sqlite3.connect(self.database)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Commit and close the connection.

        Args:
            exc_type: type of the exception raised if any
            exc_value: exception raised if any
            traceback: trace of the exception raised if any
        """
        if not self.conn:
            return

        if exc_value:
            log.error(
                'An error happend within the DateDb context, rolling back',
                stack_info=True,
            )
            self.conn.rollback()
        else:
            log.info('Committing changes')
            self.conn.commit()
        self.conn.close()


class DateDb(DbContextManager):
    """Context manager to manipulate the birthdays in the database."""

    no_connection_error = 'No active DB connection.'

    def init_birthday_db(self) -> None:
        """Initialize the database meant to gather birthday dates."""
        if not self.conn:
            log.warning(self.no_connection_error)
            return

        cursor = self.conn.cursor()

        # Create birthday table if not existing
        request = """
        CREATE TABLE IF NOT EXISTS birthday_table (
            user INTEGER PRIMARY KEY,
            birthday TEXT
        )
        """
        cursor.execute(request)

    def update_birthday(self, user: int, birthday: str) -> None:
        """Add or modify the birthday of the wanted user.

        Args:
            user: discord identifier of the user
            birthday: birthday date of the user ('dd-mm')
        """
        if not self.conn:
            log.warning(self.no_connection_error)
            return

        cursor = self.conn.cursor()

        # Update birthday for specified user
        request = """INSERT OR REPLACE INTO birthday_table
                    (user, birthday) VALUES (?,?)"""
        cursor.execute(request, (user, birthday))

    def remove_birthday(self, user: int) -> None:
        """Remove the birthday of the wanted user.

        Args:
            user: discord identifier of the user
        """
        if not self.conn:
            log.warning(self.no_connection_error)
            return

        cursor = self.conn.cursor()

        # Delete birthday for specified user
        request = """
        DELETE FROM birthday_table WHERE user=?
        """
        cursor.execute(request, (user,))

    def get_birthdays(self, date: datetime.date) -> list[int]:
        """Get the users whose birthdays are on given date.

        Args:
            date: the date on which we want to know who were born

        Returns:
            the list of users who were born on date,
            empty if no users were born
        """
        if not self.conn:
            log.warning(self.no_connection_error)
            return []

        cursor = self.conn.cursor()

        # Get the list of birthdays
        request = """
            SELECT user FROM birthday_table WHERE birthday=?
        """
        cursor.execute(request, (date.isoformat(),))

        return [user_record[0] for user_record in cursor]

    def get_all_birthdays(self) -> list[Birthday]:
        """Get all the birthdays.

        Returns:
            the list of bithday's tuples
        """
        if not self.conn:
            log.warning(self.no_connection_error)
            return []

        cursor = self.conn.cursor()

        # Get the list of users
        request = """
        SELECT user, birthday FROM birthday_table
        ORDER BY birthday
        """
        cursor.execute(request)

        return [Birthday(*record) for record in cursor]


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
    return date.date().isoformat()
