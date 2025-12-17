from enum import Enum

class CardType(Enum):
    BASEBALL = "baseball"
    FOOTBALL = "football"
    BASKETBALL = "basketball"
    POKEMON = "pokemon"
    MAGIC = "magic"
    ONE_PIECE = "one_piece"

class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"