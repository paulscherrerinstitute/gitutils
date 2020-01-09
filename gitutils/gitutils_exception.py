#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys


class NoTraceBackWithLineNumber(Exception):
    def __init__(self, msg):
        self.args = "{0.__name__} : {1}".format(type(self), msg),
        sys.exit(self)


class GitutilsError(NoTraceBackWithLineNumber):
    pass

class GitutilsWarning(NoTraceBackWithLineNumber):
    pass

class GitutilsDebug(NoTraceBackWithLineNumber):
    pass
