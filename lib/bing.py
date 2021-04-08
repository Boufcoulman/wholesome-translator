"""Interface to Bing's tranlation API."""

import json
from functools import lru_cache

from requests import post

default_headers = {
    'Host': 'www.bing.com',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'https://www.bing.com/',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Connection': 'keep-alive',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
}
default_parameters = {
    'IG': '839D27F8277F4AA3B0EDB83C255D0D70',
    'IID': 'translator.5033.3',
}

translate_table = {
    'ar': 'Arabe',
    'bg': 'Bulgare',
    'ca': 'Catalan',
    'zh-Hans': 'Chinois (simplifié)',
    'zh-Hant': 'Chinois traditionnel',
    'hr': 'Croate',
    'cs': 'Tchèque',
    'da': 'Danois',
    'nl': 'Néerlandais',
    'en': 'Anglais',
    'et': 'Estonien',
    'fi': 'Finnois',
    'fr': 'Français',
    'de': 'Allemand',
    'el': 'Grec',
    'gu': 'Goudjrati',
    'ht': 'Créole haïtien',
    'he': 'Hébreu',
    'hi': 'Hindi',
    'hu': 'Hongrois',
    'is': 'Islandais',
    'id': 'Indonésien',
    'ga': 'Irlandais',
    'it': 'Italien',
    'ja': 'Japonais',
    'tlh-Latn': 'Klingon',
    'ko': 'Coréen',
    'ku-Arab': 'Kurde (central)',
    'lv': 'Letton',
    'lt': 'Lituanien',
    'ms': 'Malais',
    'mt': 'Maltais',
    'nb': 'Norvégien',
    'ps': 'Pachto',
    'fa': 'Persan',
    'pl': 'Polonais',
    'pt': 'Portugais',
    'ro': 'Roumain',
    'ru': 'Russe',
    'sr-Cyrl': 'Serbe (cyrillique)',
    'sr-Latn': 'Serbe (latin)',
    'sk': 'Slovaque',
    'sl': 'Slovène',
    'es': 'Espagnol',
    'sw': 'Swahili',
    'sv': 'Suédois',
    'ty': 'Tahitien',
    'th': 'Thaï',
    'tr': 'Turc',
    'uk': 'Ukrainien',
    'ur': 'Ourdou',
    'vi': 'Vietnamien',
    'cy': 'Gallois',
    'yua': 'Yucatec Maya',
}


MAX_CACHE = 5000


class SourceExample(object):
    """Example use of a text in the source language."""

    def __init__(self, example_json) -> None:
        """Initialise the source example.

        Args:
            example_json: body of the response from Bing
        """
        self.prefix = example_json.get('sourcePrefix', '')
        self.term = example_json.get('sourceTerm', '')
        self.suffix = example_json.get('sourceSuffix', '')
        self.example = self.prefix + self.term + self.suffix

    def __repr__(self) -> str:
        """Full source example.

        Returns:
            the complete example
        """
        return str(self.example)


class DestinationExample(object):
    """Example use of a text in the target language."""

    def __init__(self, example_json) -> None:
        """Initialise the target example.

        Args:
            example_json: body of the response from Bing
        """
        self.prefix = example_json.get('targetPrefix', '')
        self.term = example_json.get('targetTerm', '')
        self.suffix = example_json.get('targetSuffix', '')
        self.example = self.prefix + self.term + self.suffix

    def __repr__(self) -> str:
        """Full target example.

        Returns:
            the complete example
        """
        return str(self.example)


class Example(object):
    """Example use of a text in both soure and target languages."""

    def __init__(self, example_json) -> None:
        """Initialise the example.

        Args:
            example_json: body of the response from Bing
        """
        self.source = SourceExample(example_json)
        self.destination = DestinationExample(example_json)

    def __repr__(self) -> str:
        """Full source example.

        Returns:
            the complete source example
        """
        return str(self.source)


class BingTranslate(object):
    """A Python implementation of Microsoft Bing Translation's APIs."""

    def example(self, text, destination_language, source_language=None):
        """Return examples for the given text.

        Args:
            text: text that we want to have examples of
            destination_language: language we want to see examples of
            source_language: langue of `text`, autodetected if None

        Returns:
            examples of the translation of `text` in target language
        """
        if source_language is None:
            source_language = self.language(text)
        if source_language is None:
            return None

        translation = self.translate(
            text,
            destination_language,
            source_language,
        )
        if translation is None:
            return None

        try:
            response = post(
                'https://www.bing.com/texamplev3',
                headers=default_headers,
                params=default_parameters,
                data={
                    'text': str(text).lower(),
                    'from': str(source_language),
                    'to': str(destination_language),
                    'translation': str(translation).lower(),
                },
            )
        except Exception:
            return None
        if not response.ok:
            return None
        examples = json.loads(response.text)[0]['examples']
        return [Example(example) for example in examples]

    def spellcheck(self, text, source_language=None):
        """Check the spelling of the given text.

        Args:
            text: the text that we want to spellcheck
            source_language: language of `text`, or autodetect if None

        Returns:
            automatically corrected text
        """
        if source_language is None:
            source_language = self.language(text)
        if source_language is None:
            return None
        try:
            response = post(
                'https://www.bing.com/tspellcheckv3',
                headers=default_headers,
                params=default_parameters,
                data={'text': str(text), 'fromLang': str(source_language)},
            )
        except Exception:
            return None

        if not response.ok:
            return None

        corrected_text = json.loads(response.text)['correctedText']
        return corrected_text or text

    @lru_cache(maxsize=MAX_CACHE)
    def language(self, text):
        """Give back the language of the given text.

        Args:
            text: the original text whose language we want to detect

        Returns:
            the source language of the text
        """
        try:
            response = post(
                'https://www.bing.com/ttranslatev3',
                headers=default_headers,
                params=default_parameters,
                data={
                    'text': str(text),
                    'fromLang': 'auto-detect',
                    'to': 'en',
                },
            )
        except Exception:
            return None

        if not response.ok:
            return None
        return json.loads(response.text)[0]['detectedLanguage']['language']

    @lru_cache(maxsize=MAX_CACHE)
    def translate(self, text, destination_language, source_language=None):
        """Translate the given text to the given language.

        Args:
            text: the text to translate
            destination_language: the language to translate into
            source_language: the text's language, or autodetect if it's None

        Returns:
            translated text if all went well or None otherwise
            source language if all went well or None otherwise
        """
        if source_language is None:
            source_language = 'auto-detect'
        try:
            response = post(
                'https://www.bing.com/ttranslatev3',
                headers=default_headers,
                params=default_parameters,
                data={
                    'text': str(text),
                    'fromLang': str(source_language),
                    'to': str(destination_language),
                },
            )
        except Exception:
            return (None, None)

        if not response.ok:
            return (None, None)

        src_lang = translate_table[
            json.loads(response.text)[0]['detectedLanguage']['language']
        ]
        return (
            json.loads(response.text)[0]['translations'][0]['text'],
            src_lang,
        )
