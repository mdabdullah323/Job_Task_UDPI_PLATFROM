from enum import Enum


class UserChoice(Enum):
    PARENT = "1"
    CHILD = "2"


class ApiOperation(Enum):
    CREATE = "1"
    UPDATE = "2"
    DELETE = "3"


class Status(Enum):
    CRATED = 1
    UPDATED = 2
    DELETED = 3
    Failed = 4
