from __future__ import absolute_import, division, with_statement


class PyddosdException(Exception):
    pass

class RouterException(PyddosdException):
    pass

class TerminalExceptionError(RouterException):
    pass


