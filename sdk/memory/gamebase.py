from . import Base
from ..constants.osumodes import OsuMode

class GameBase(Base):
    def __init__(self):
        super().__init__()

    @property
    def time(self) -> int:
        """Property to get the current game time."""
        try:
            # [[GameBase::Time] + 0] + 0
            time_offset = self.memory.offsets.get("GameBase::Time")
            if not time_offset:
                return 0
            # [[GameBase::Time] + 0] + 0
            time_ptr = self.memory.read_int(time_offset)
            if not time_ptr:
                return 0
            # [[GameBase::Time] + 0] + 0
            return self.memory.read_int(time_ptr)
        except:
            return 0

    @property
    def mode(self) -> OsuMode:
        """Property to get the current game mode."""
        try:
            # [[GameBase::Mode] + 0] + 0
            mode_offset = self.memory.offsets.get("GameBase::Mode")
            if not mode_offset:
                return OsuMode(0)
            # [[GameBase::Mode] + 0] + 0
            mode_ptr = self.memory.read_int(mode_offset)
            if not mode_ptr:
                return OsuMode(0)
            # [[GameBase::Mode] + 0] + 0
            return OsuMode(self.memory.read_int(mode_ptr))
        except:
            return OsuMode(0)