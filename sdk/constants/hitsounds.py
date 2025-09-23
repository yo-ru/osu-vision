from enum import IntEnum, unique


@unique
class HitSounds(IntEnum):
    NONE = 0
    NORMAL = 1
    WHISTLE = 2
    FINISH = 4
    CLAP = 8
