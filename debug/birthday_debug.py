from dateutil.parser import parse
import datetime

MOIS = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
        'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
        ]


def update(user, *date_input):
    date = parse(' '.join(date_input), dayfirst=True, yearfirst=False)
    if date:
        print(date)
        print(f"Anniversaire enregistré le {date.day} {MOIS[date.month-1]}")
        check_if_birthday(date)


def check_if_birthday(date):
    print(f"Date du jour : {datetime.datetime.now()}")


if __name__ == "__main__":
    update("oui", "04", "07")
