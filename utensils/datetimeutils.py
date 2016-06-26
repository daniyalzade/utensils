# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time
from datetime import datetime


def epoch(dt=None):
    if not dt:
        dt = datetime.utcnow()
    return int(time.mktime(dt.timetuple()) * 1000 + (dt.microsecond / 1000))
