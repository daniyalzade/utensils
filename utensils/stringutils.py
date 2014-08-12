# This Python file uses the following encoding: utf-8
import logging
import HTMLParser
import posixpath
import random
import re
import string

PHONE_NUMBER_PATTERN = re.compile(r'(\d{3})[-).(] *(\d{3})[-.](\d{4})')

TURKISH_TO_LATIN_CHAR_MAP = {
        u'ç':u'c',
        u'ı':u'i',
        u'ğ':u'g',
        u'ö':u'o',
        u'ü':u'u',
        u'ş':u's',
        u'â':u'a',
        }

def generate_str(size=32, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def string_contains(string, keywords, lower=True, full_word=False):
    """
    @param word: str
    @param keywords: list(str), check if any one of the keywords matches
    @param lower: bool
    @param full_word: bool, only return true if string contains a full_word
    that matches one of the keywords
    @return: bool
    """
    if not string:
        return False
    if lower:
        string = string.lower()
        words = [w.lower() for w in keywords]
    if not full_word:
        return bool([w for w in words if w in string])
    for keyword in keywords:
        for word in string.split():
            if word == keyword:
                return True
    return False

def _callback(matches):
    id = matches.group(1)
    try:
        return unichr(int(id))
    except:
        return id

def decode_unicode_references(data):
    return re.sub("&#(\d+)(;|(?=\s))", _callback, data)

def basename(path, ext=True):
    """
    @param path: str
    @param ext: bool, whether or not to return the extension
    @return: bool
    """
    name = posixpath.basename(path)
    if not ext:
        name = posixpath.splitext(name)[0]
    return name

def is_upper(s):
    """
    @param s: str
    @return: bool
    """
    if not s:
        return False
    return all(map(lambda c: c.isalpha() and c.istitle(), s))

def parse_int_or_string(val):
    """
    @param val: str
    @return: int|str|None
    """
    if not val:
        return val
    try:
        return int(val)
    except:
        return val

def parse_price(price, fun=max):
    """
    @param price: str
    @param fun: max | min : determine max or min of price range when there is conflicts
    @return: float
    taking
    """
    price = price.lower().replace('for', '|')
    price = re.sub('[\(\)a-z\s$&;:]', '', price.lower())
    # Strip leading / trailing .'s
    price = price.strip('.')
    # Combine comma-separation used for denoting 000s
    if '|' in price:
        quantity, amount = price.split('|')
        return float(amount) / float(quantity)
    return float(fun(price.replace(',', '').split('-'))) #'$308.00 - $440.00'

def normalize(s):
    """
    @param str: s
    @return: str
    """
    if not s:
        return s
    s = s.replace('&amp;', '&')
    s = s.replace('&nbsp;', ' ')
    s = s.strip().lower()
    return s

def unformat_phone_number(phone):
    """
    input: 516.873.7380 output: 5168737380
    input: 516-873-7380 output: 5168737380
    input: (212) 431-2686 output: 2124312686
    """
    phone = phone.replace(' ', '')
    h = HTMLParser.HTMLParser()
    phone = h.unescape(phone)
    match = PHONE_NUMBER_PATTERN.search(phone)
    if match:
        return ''.join(match.groups())
    phone = re.sub(r'[^\d]+', '', phone)

    if phone and phone[0] == '1':
        phone = phone[1:]

    if len(phone) != 10:
        raise ValueError("phone number %s is not 10 digits long, potential error" % phone)
    return phone

def to_upper_first_chars(str_):
    return ' '.join([word.capitalize() for word in str_.lower().split(' ')])

def to_latin(str_):
    for t_char, l_char in TURKISH_TO_LATIN_CHAR_MAP.items():
        str_ = str_.replace(t_char, l_char)
    return str_

def to_float(str_):
    """
    @param str_: str
    @return: float
    """
    return float(str_) if str_ else None

def to_array(str_, delimeter=','):
    """
    @param str_: str
    @param delimeter: str
    @return: list
    """
    if not str_:
        return []
    return str_.split(delimeter)

def to_bool(str_):
    """
    Convert various input for specifying a boolean to a Bool.

    @param str_: str, input to parse
    @return: bool
    """

    if str_ in [True, 1, 'True', 'true', '1']:
        return True

    if str_ in [None, False, 0, 'False', 'false', '0']:
        return False

    # As a last resort try interpreting as a number, letting it
    # throw an exception if it doesn't work.
    try:
        return int(str_) != 0
    except:
        return False

def _suffix(d):
    return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')

def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + _suffix(t.day))

def slugify(n):
    """
    TODO: Normally do not use this, and use django's version. We are using
    it here for backwards compatibality.

    @param n: str
    @return: str
    """
    n = re.sub(r'[^a-zA-Z0-9 ]', '', n)
    n = re.sub(r'\s+', '-', n).lower()
    return n
