from googletrans import LANGUAGES

from json import loads
from requests import get
from operator import add
from functools import reduce

message = 'Der blaue Tropfen fließt auf die rote Seerose. como estas. '
request_result = get("https://translate.googleapis.com/translate_a/single?client=gtx&dt=t&sl=auto&tl=fr&q=" + message)
translated_text = loads(request_result.text)
src_lang = LANGUAGES[translated_text[2]]
fr_texts = [sentence[0] for sentence in translated_text[0]]

print(fr_texts)
print(translated_text)
print(f'"{message}" traduit du "{src_lang.capitalize()}" en "{reduce(add,[text for text in fr_texts])}"')


# translator = Translator()
# translator.translate('안녕하세요.')


# acquirer = TokenAcquirer()
# text = 'test'
# tk = acquirer.do(text)
# print(tk)
