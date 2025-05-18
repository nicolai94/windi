from enum import Enum


class ChatType(str, Enum):
    PRIVATE = "PRIVATE"
    GROUP = "GROUP"
