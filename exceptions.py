class ExitException(Exception):
    pass


class InvalidUser(ExitException):
    pass


class DuplicateEntry(Exception):
    pass
