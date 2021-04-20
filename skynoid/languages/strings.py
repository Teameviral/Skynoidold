from codecs import decode
from codecs import encode

import yaml

from skynoid import logging as LOGGER
from skynoid import Owner
from skynoid.plugins.database.lang_db import prev_locale

LANGUAGES = [
    'en-US'
]
  
try:
    strings = {
        i: yaml.full_load(
            open('locales/' + i + '.yml'),
        ) for i in LANGUAGES
    }
except UnicodeDecodeError:
    strings = {
        i: yaml.full_load(
            open('locales/' + i + '.yml', encoding='utf8'),
        ) for i in LANGUAGES
    }
    
def tld(t, _show_none=True):
    LANGUAGE = prev_locale(Owner)
    if LANGUAGE:
        LOCALE = LANGUAGE.locale_name
        if LOCALE in ('en-US') and t in strings['en-US']:
            result = decode(
                encode(strings['en-US'][t], 'latin-1', 'backslashreplace'),
                'unicode-escape',
            )
    if t in strings['en-US']:
        result = decode(
            encode(
                strings['en-US'][t],
                'latin-1',
                'backslashreplace',
            ),
            'unicode-escape',
        )
        return result
        
    err = f'No string found for {t}.\nReport it in @SkynoidSupport.'
    LOGGER.warning(err)
    return err
    
def tld_list(t):
    LANGUAGE = prev_locale(Owner)

    if LANGUAGE:
        LOCALE = LANGUAGE.locale_name
        if LOCALE in ('en-US') and t in strings['en-US']:
            return strings['en-US'][t]
            
    if t in strings['en-US']:
        return strings['en-US'][t]

    LOGGER.warning(f'#NOSTR No string found for {t}.')
    return f'No string found for {t}.\nReport it in @SkynoidSupport.'
