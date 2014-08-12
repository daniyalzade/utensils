"""A collection of dict tools.
"""
from collections import OrderedDict
from copy import copy
import operator
import re

from utensils.stringutils import normalize

ARRAY_ACCESSOR = re.compile(r'(.*)\[(.*?)\]')

def flatten(dict_, key='children', children=[]):
    """
    Flattens nested dictionaries that have a nesting structure based on key.

    @param dict_: dict, starting with the parent node
    @param key: str, key on which to look for the children
    @return: list, list of children
    """
    flat = []
    if key in dict_:
        for child in dict_[key]:
            flat.extend(flatten(child, key))
        del(dict_[key])
    flat.append(dict_)
    return flat

def inverse(dict_):
    """
    @param dict_: dict
    @return dict_
    """
    return dict((v,k) for k, v in dict_.iteritems())

def order(dict_, by_value=False, reverse=False):
    """
    @param dict_: dict
    @param by_value: bool
    @return: dict_
    """
    def _getter(t):
        return t[1] if by_value else t[0]
    return OrderedDict(sorted(dict_.items(),
        key=_getter,
        reverse=reverse,
        ))

def transform(dict_, mapper, clone=False):
    """
    Transform the dict with the path mapping rules passed in the mapper. Does
    not modify the passed in dict_

    @param dict_, dict
    @param mapper, dict(key, value)
    @param clone: bool, clone initial dict and start writing on it as opposed
    to starting with an empty dict.
    @return dict_
    """

    data = copy(dict_) if clone else {}
    for from_path, to_path in mapper.items():
        set_dotted(data, to_path, get_dotted(dict_, from_path))
    return data

def get_dotted(data, field, default=None, delimiter='.',
        do_normalize=False,
        ):
    """
    Get a nested subfield inside data using Mongo style dotted notation
    notation. For example:
        data = {'a': 1, 'b': {'c': 2, 'd': {'e': 3}}}
        get_dotted_field(data, 'b.d.e') => 3

    Also allows array accessors:
        foo[@bla=3].bar: Choose the element in foo, whose attribute bla equals 3
        foo[3].bar: Choose index 3 in the foo array.

    Note that it is type insensitive, i.e. in comparisions '3' and 3 will
    evaluate to the same.
    """
    components = field.split(delimiter)
    components.reverse()
    while components and isinstance(data, dict):
        component = components.pop()
        accessor = None
        match = re.match(ARRAY_ACCESSOR, component)
        if match:
            component = match.group(1)
            accessor = match.group(2)
        data = data.get(component)
        if accessor:
            # Dict accessor
            if "@" in accessor:
                params = {}
                for pairs in accessor.split('@')[1:]:
                    params[pairs.split('=')[0]] = pairs.split('=')[1]
                # Kind of hacky, but let's handle the case where this should
                # be a list, but turns out a dict, such as in Gap's case.
                data = data if isinstance(data, list) else [data]
                for item in data:
                    for key, value in params.items():
                        if do_normalize:
                            val1 = normalize(str(item[key]))
                            val2 = normalize(str(value))
                        else:
                            val1 = str(item[key])
                            val2 = str(value)
                        if val1 != val2:
                            break
                    # If we iterated over all the params, and did not break
                    # then we are good.
                    else:
                        data=item
                        break

            # List accessor
            elif "*" in accessor:
                cur_fields = delimiter.join(components[::-1])
                return [get_dotted(d, cur_fields) for d in data]
            else:
                data = operator.getitem(data, int(accessor))

    # If there are components left, the final dest wasn't reached.
    if components or data == None:
        return default
    return data

def set_dotted(data, field, value, delimiter='.'):
    """Set a nested subfield inside data using Mongo style dotted notation
    notation. For example:
        data = {'a': 1, 'b': {'c': 2, 'd': {'e': 3}}}
        set_dotted_field(data, 'b.d.e', 4)
        data == {'a': 1, 'b': {'c': 2, 'd': {'e': 4}}}
    """
    if not delimiter in field:
        data[field] = value
    else:
        next_field, remaining_fields = field.split(delimiter, 1)

        # If next_field isn't there, create it so we can move on.
        if next_field not in data:
            data[next_field] = {}

        set_dotted(data[next_field], remaining_fields, value, delimiter=delimiter)

def unicode_keys(data):
    return apply_to_dict(data,
                         lambda x: unicode(x) if isinstance(x,str) else x)

def apply_to_dict(data, _function):
    if type(data) == dict:
        data = dict(data) # copy it first
        for key in data:
            data[key] = apply_to_dict(data[key], _function)
    elif type(data) == list:
        data = list(data) # copy it first
        for i, item in enumerate(data):
            data[i] = apply_to_dict(item, _function)
    else:
        data = _function(data)
    return data

def replace_unicode_keys(data, recurse=False):
    """ Convert top-level unicode strings to regular strings so the
    dict can be passed as keyword args

    @param data: Dict to replace unicode keys of.
    @param recurse: Recursively replace sub-dicts. Default: False
    """
    # Copy dict so original isn't modified.
    if not recurse:
        return dict([(str(key), data[key]) for key in data])
    new_data = {}
    for key in data:
        if type(data[key]) == dict:
            new_data[str(key)] = replace_unicode_keys(data[key], recurse=True)
        else:
            new_data[str(key)] = data[key]
    return new_data

def dict_without_keys(src_dict, keys_to_exclude):
    """Copies a dict, leaving out some keys if there.

    @param src_dict: Dict to copy.
    @param keys_to_exclude: A list of keys to exclude. All these don't have to
        be in the src_dict. They'll be ignored if they're not.
    @return: A copy of src_dict without keys_to_exclude.
    """
    return dict( (key, value) for key, value in src_dict.iteritems() if key not in keys_to_exclude )

def get_from_list(items, key, value, default=None):
    """Get an item from a list of collections based on a key/value.

    @param items: A list of collections.
    @param key: The key to look up in the items in the list.
    @return: The first item that has the given key with the given value, or the default.
    """
    for item in items:
        try:
            if item[key] == value:
                return item
        except KeyError:
            pass
    return default

def to_dict_by_key(col, key_key, value_key=None, include_key=False):
    """
    Turn a list of collections into a dict by a key in the items, optionally
    only using a value.
    Ex:
      col = [{'k': 'a', 'n': 1}, {'k': 'b', 'n': 2}, {'n': 3}]
      to_dict_by_key(col, 'k') --> {'a': {'n': 1}, 'b': {'n': 2}}
      to_dict_by_key(col, 'k', include_key=True) --> {'a': {'k': 'a', 'n': 1}, 'b': {'k': 'b', 'n': 2}}
      to_dict_by_key(col, 'k', 'v') --> {'a': 1, 'b': 2}

    Items that don't contain key are ignored.

    @param col: collection, Collection to turn into a dict.
    @param key_key: str, Key to look for in items and turn into keys in resulting dict.
    @param value_key: Key to look for in items and turn into values in resulting dict.
    @return: A dict keyed by things in the collection.
    """
    if value_key != None:
        return dict( (item[key_key], item[value_key]) for item in col if key_key in item )
    elif not include_key:
        return dict( (item[key_key], dict_without_keys(item, [key_key])) for item in col if key_key in item )
    else:
        return dict( (item[key_key], item) for item in col if key_key in item )

def combine_dicts(dicts, fn=lambda values: sum(values), default=None):
    """Combine values of multiple dicts into one using a function.
    If no default is given, keys that are missing from one or more dicts are
    ignored.

    @param dicts: A collection of dicts to combine.
    @param fn: The function to run over multiple values from the dicts for each
        key, before putting into combined dict.
    @param default: For dicts that don't have a particular key, use this value
        before passing into fn for combining. If default == None, ignore the
        entire key (don't include in combined dict) if any input dicts don't
        have the key.
    @return: A dict containing the combination of the input dicts.
    """
    # Copy dicts in case it's a generator.
    dicts = list(dicts)
    if default == None:
        all_keys = reduce(lambda a,b: set(a).intersection(b), (d.keys() for d in dicts))
        return dict( (key, fn([d[key] for d in dicts])) for key in all_keys )
    else:
        all_keys = reduce(lambda a,b: set(a).union(b), (d.keys() for d in dicts))
        return dict( (key, fn([d.get(key, default) for d in dicts])) for key in all_keys )

def deep_items(d, delimeter='.'):
    """
    Travsere the dict (which could be a dict of dicts) and return a list of
    path, value pairs.

    @param d: dict
    @param delimterer: str, optional.
    @return: list(str, Object)
    """
    pairs = []
    for k, v in d.items():
        if isinstance(v, dict):
            cur_pairs = deep_items(v, delimeter)
            pairs.extend([(k + delimeter + cur_k, cur_v) for (cur_k, cur_v) in cur_pairs])
        else:
            pairs.append((k, v))
    return pairs

def get_value_for_key(data, key):
    """
    Recursively iterate over a dict to find the value for a key

    @param data: dict
    @param key: str
    @return: Object
    """
    if isinstance(data, dict):
        for cur_key, val in data.items():
            if cur_key == key:
                return val
            to_return = get_value_for_key(val, key)
            if to_return:
                return to_return
    elif isinstance(data, list):
        for item in data:
            to_return = get_value_for_key(item, key)
            if to_return:
                return to_return
    return None
