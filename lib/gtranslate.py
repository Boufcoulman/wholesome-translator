"""Interface to Google translate API."""

import json
from functools import lru_cache
from requests import get
from operator import add
from functools import reduce

translate_table = {
    'af': 'Afrikaans',
    'sq': 'Albanais',
    'de': 'Allemand',
    'am': 'Amharique',
    'en': 'Anglais',
    'ar': 'Arabe',
    'hy': 'Arménien',
    'az': 'Azéri',
    'eu': 'Basque',
    'bn': 'Bengali',
    'my': 'Birman',
    'be': 'Biélorusse',
    'bs': 'Bosnien',
    'bg': 'Bulgare',
    'ca': 'Catalan',
    'ceb': 'Cebuano',
    'zh-CN ou zh': 'Chinois (simplifié)',
    'zh-TW': 'Chinois (traditionnel)',
    'co': 'Corse',
    'ko': 'Coréen',
    'hr': 'Croate',
    'ht': 'Créole haïtien',
    'da': 'Danois',
    'eo': 'Espéranto',
    'et': 'Estonien',
    'fi': 'Finnois',
    'fr': 'Français',
    'fy': 'Frison',
    'gl': 'Galicien',
    'cy': 'Gallois',
    'gd': 'Gaélique (Écosse)',
    'el': 'Grec',
    'gu': 'Gujarati',
    'ka': 'Géorgien',
    'ha': 'Haoussa',
    'haw': 'Hawaïen',
    'hi': 'Hindi',
    'hmn': 'Hmong',
    'hu': 'Hongrois',
    'he ou iw': 'Hébreu',
    'ig': 'Igbo',
    'id': 'Indonésien',
    'ga': 'Irlandais',
    'is': 'Islandais',
    'it': 'Italien',
    'ja': 'Japonais',
    'jv': 'Javanais',
    'kn': 'Kannada',
    'kk': 'Kazakh',
    'km': 'Khmer',
    'rw': 'Kinyarwanda',
    'ky': 'Kirghyz',
    'ku': 'Kurde',
    'lo': 'Laotien',
    'la': 'Latin',
    'lv': 'Letton',
    'lt': 'Lituanien',
    'lb': 'Luxembourgeois',
    'mk': 'Macédonien',
    'ms': 'Malais',
    'ml': 'Malayâlam',
    'mg': 'Malgache',
    'mt': 'Maltais',
    'mi': 'Maori',
    'mr': 'Marathi',
    'mn': 'Mongol',
    'no': 'Norvégien',
    'ny': 'Nyanja (Chichewa)',
    'nl': 'Néerlandais',
    'ne': 'Népalais',
    'or': 'Odia (Oriya)',
    'uz': 'Ouzbek',
    'ug': 'Ouïghour',
    'ps': 'Pachtô',
    'pa': 'Panjabi',
    'fa': 'Perse',
    'pl': 'Polonais',
    'pt': 'Portugais(Portugal, Brésil)',
    'ro': 'Roumain',
    'ru': 'Russe',
    'sm': 'Samoan',
    'sr': 'Serbe',
    'st': 'Sesotho',
    'sn': 'Shona',
    'sd': 'Sindhî',
    'si': 'Singhalais',
    'sk': 'Slovaque',
    'sl': 'Slovène',
    'so': 'Somali',
    'su': 'Soundanais',
    'es': 'Spanish',
    'sv': 'Suédois',
    'sw': 'Swahili',
    'tg': 'Tadjik',
    'tl': 'Tagalog (philippin)',
    'ta': 'Tamoul',
    'tt': 'Tatar',
    'cs': 'Tchèque',
    'th': 'Thaï',
    'tr': 'Turc',
    'tk': 'Turkmène',
    'te': 'Télougou',
    'uk': 'Ukrainien',
    'ur': 'Urdu',
    'vi': 'Vietnamien',
    'xh': 'Xhosa',
    'yi': 'Yiddish',
    'yo': 'Yoruba',
    'zu': 'Zulu',
}


MAX_CACHE = 5000


@lru_cache(maxsize=MAX_CACHE)
def translate(text, dest_lang, src_lang=None):
    """Translate the given text to the given language.

    Args:
        text: the text to translate
        dest_lang: the language to translate into
        src_lang: the text's language, or autodetect if it's None

    Returns:
        translated text if all went well or None otherwise
        source language if all went well or None otherwise
    """
    if src_lang is None:
        src_lang = 'auto'

    base_url = 'https://translate.googleapis.com/translate_a/single'
    params = {
        'client': 'gtx',
        'dt': 't',
        'sl': src_lang,
        'tl': dest_lang,
        'q': text,
    }

    try:
        response = get(url=base_url, params=params)
    except Exception:
        return None

    if not response.ok:
        return None

    json_response = json.loads(response.text)

    detected_lang = translate_table[
        json_response[2]
    ]

    translated_texts = [sentence[0] for sentence in json_response[0]]
    translated_msg = reduce(add, [sentence for sentence in translated_texts])

    return (
        translated_msg,
        detected_lang,
    )
