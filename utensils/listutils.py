from collections import defaultdict
from itertools import cycle
from itertools import islice
from itertools import groupby
import logging
import random

def shuffle_multi(*args, **kwargs):
    """
    Shuffle function that does not do in place, and can have a determenistic
    seed.

    @param items: list(int)
    @param seed: int
    @return: list(int)...
    """
    assert(args)
    # Check that all the members have the same size
    assert(len(set(map(len, args))) == 1)

    if not len(args[0]):
        return args
    seed = kwargs.get('seed')
    generator = random.Random()
    generator.seed(seed)
    to_return = zip(*[t[1] for t in sorted((generator.random(), i) for i in zip(*args))])
    return [list(t) for t in to_return]

def shuffle(items, seed=None):
    """
    Shuffle function that does not do in place, and can have a determenistic
    seed.

    @param items: list(int)
    @param seed: int
    @return: list(int)
    """
    random.seed(seed)
    return [t[1] for t in sorted((random.random(), i) for i in items)]

def merge(list_1, list_2, mix_percentage=0):
    """
    @param list_1: list
    @param list_2: list
    @param mix_percentage: int, [0-100], if 0, list_1 comes first, if 100,
    list_2 comes first, ow, it's a mix
    """
    cutoff_1 = int((100 - float(mix_percentage)) / 100 * len(list_1))
    cutoff_2 = int(float(mix_percentage) / 100 * len(list_2))
    return (
            shuffle(list_1[:cutoff_1] + list_2[:cutoff_2]) +
            shuffle(list_1[cutoff_1:] + list_2[cutoff_2:])
            )

def push_to_front(l, filter_fn):
    """
    Push the first matching item to the first of the list

    @param l: list
    @param filter_fn: lambda Object
    @return: list
    """
    idx = find(l, filter_fn)
    if not idx:
        return l
    return [l[idx]] + l[:idx] + l[idx+1:]

def find(l, filter_fn):
    """
    Return the index of the first matching item, else None

    @param l: list
    @param filter_fn: lambda Object
    @return: int|None
    """
    for idx, item in enumerate(l):
        if filter_fn(item):
            return idx
    return None

def batch(arr, size):
    cur_arr = []
    for item in arr:
        cur_arr.append(item)
        if len(cur_arr) >= size:
            yield cur_arr
            cur_arr = []
    if cur_arr:
        yield cur_arr

def flatten(x):
    result = []
    for el in x:
        if hasattr(el, "__iter__") and not isinstance(el, basestring) and not isinstance(el, dict):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result

def _display_msg(msg, use_print=False):
    """
    @param msg: str
    @param use_print: bool
    """
    if use_print:
        print msg
        return
    logging.info(msg)

def adv_enumerate(list_,
        start=0,
        end=None,
        frequency=100,
        use_print=False,
        get_tuple=False,
        msg=None,
        ):
    """
    @param list_: list
    @param frequency: int
    @param use_print: bool
    @param msg: str, addition information
    @return: Generator
    """
    len_ = 'NA'
    try:
        len_ = len(list_)
    except TypeError:
        try:
            len_ = list_.count()
        except Exception:
            pass
    for i, item in enumerate(list_, start=start):
        if not i % frequency:
            to_print = "completed %s/%s" % (i, len_)
            if msg:
                to_print = "%s, %s" % (to_print, msg)
            _display_msg(to_print)
        if end and i >= end:
            raise StopIteration
        yield (i, item) if get_tuple else item

## {{{ http://code.activestate.com/recipes/576694/ (r9)
import collections

class OrderedSet(collections.MutableSet):

    def __init__(self, iterable=None):
        self.end = end = []
        end += [None, end, end]         # sentinel node for doubly linked list
        self.map = {}                   # key --> [key, prev, next]
        if iterable is not None:
            self |= iterable

    def __len__(self):
        return len(self.map)

    def __contains__(self, key):
        return key in self.map

    def add(self, key):
        if key not in self.map:
            end = self.end
            curr = end[1]
            curr[2] = end[1] = self.map[key] = [key, curr, end]

    def discard(self, key):
        if key in self.map:
            key, prev, next = self.map.pop(key)
            prev[2] = next
            next[1] = prev

    def __iter__(self):
        end = self.end
        curr = end[2]
        while curr is not end:
            yield curr[0]
            curr = curr[2]

    def __reversed__(self):
        end = self.end
        curr = end[1]
        while curr is not end:
            yield curr[0]
            curr = curr[1]

    def pop(self, last=True):
        if not self:
            raise KeyError('set is empty')
        key = self.end[1][0] if last else self.end[2][0]
        self.discard(key)
        return key

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and list(self) == list(other)
        return set(self) == set(other)

def split(l, split_fn):
    """
    Take a list, and break it into list of lists based on the has value
    that is return by split_fn.

    @param l: list
    @param split_fn: func
    @return: list(list)
    """
    data = defaultdict(list)
    for item in l:
        data[split_fn(item)].append(item)
    return data.values()


def roundrobin(*iterables):
    "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
    # Recipe credited to George Sakkis
    pending = len(iterables)
    nexts = cycle(iter(it).next for it in iterables)
    while pending:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            pending -= 1
            nexts = cycle(islice(nexts, pending))

def dedup(l, fn=None):
    seen = set()
    to_return = []
    for i in l:
        if fn:
            if not fn(i) in seen:
                to_return.append(i)
                seen.add(fn(i))
        else:
            if not i in seen:
                to_return.append(i)
                seen.add(i)
    return to_return

def get_iterable_len(i):
    """
    @return: int
    """
    if (isinstance(i, list)):
        return len(i)
    return i.count()

def to_multilist(l, cols, rows=None):
    """
    @param l: list
    @param rows: int
    @param cols: int
    @return: list(list)
    """
    if not l or not cols:
        return l
    idx = 0
    to_return = []
    limit = len(l)
    if rows:
        limit = min(len(l), rows * cols)
    while idx < limit:
        to_return.append(l[idx:idx + cols])
        idx += cols
    return to_return
