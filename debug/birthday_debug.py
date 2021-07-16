from dateutil.parser import parse
import datetime

MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin',
        'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'
        ]


def update(user, *date_input):

    # Vérification du format de la date
    try:
        date = parse(' '.join(date_input), dayfirst=True, yearfirst=False)
        print(date)
        print("Anniversaire enregistré le "
              f"{date.day} {MOIS[date.month-1].capitalize()}"
              )
        check_if_birthday(date)
        return date

    except Exception:
        print("Format de date non reconnu !"
              "Veuillez saisir avec le formalisme jj-mm"
              )
        return None


def check_if_birthday(date):
    print(f"Date du jour : {datetime.datetime.now()}")


def check_if_month(month_name):
    month_name = month_name.lower()
    if month_name in MOIS:
        month = MOIS.index(month_name) + 1
        return month
    else:
        return None


def input_parse(*date_input):
    date_input = [str(check_if_month(elem)) if check_if_month(elem) else elem
                  for elem in date_input]
    print(date_input)


if __name__ == "__main__":
    # update("oui", "11-05")
    # print(check_if_month('janvier'))
    input_parse("11 05")
