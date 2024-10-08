from enum import Enum, auto

class Status(Enum):
    """
    Een enumeratie om de status van het berekenen van afstanden aan te geven.
    """
    PREPARING = auto()
    CALCULATING = auto()
    FINISHED = auto()
    MODIFYING = auto()
