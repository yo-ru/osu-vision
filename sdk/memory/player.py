from . import Base
from ..constants import GameMode

class Player(Base):
    def __init__(self):
        super().__init__()

    @property
    def failed(self) -> bool:
        """Property to check if the player has failed."""
        try:
            # [[Player::Failed] + 0] + 0
            failed_offset = self.memory.offsets.get("Player::Failed")
            if not failed_offset:
                return False
            failed_ptr = self.memory.read_int(failed_offset)
            if not failed_ptr:
                return False
            return self.memory.read_bool(failed_ptr)
        except:
            return False

    @property
    def retrying(self) -> bool:
        """Property to check if the player is retrying."""
        try:
            # [[Player::Retrying] + 0] + 0
            retrying_offset = self.memory.offsets.get("Player::Retrying")
            if not retrying_offset:
                return False
            retrying_ptr = self.memory.read_int(retrying_offset)
            if not retrying_ptr:
                return False
            return self.memory.read_bool(retrying_ptr)
        except:
            return False

    @property
    def mode(self) -> GameMode:
        """Property to get the player's current gamemode."""
        try:
            # [[Player::Mode] + 0] + 0
            mode_offset = self.memory.offsets.get("Player::Mode")
            if not mode_offset:
                return GameMode(0)
            mode_ptr = self.memory.read_int(mode_offset)
            if not mode_ptr:
                return GameMode(0)
            return GameMode(self.memory.read_int(mode_ptr))
        except:
            return GameMode(0)

    @property
    def loaded(self) -> bool:
        """Property to check if the player instance is loaded."""
        try:
            # [Player::Instance] + 0x188
            instance_ptr = self.memory.resolve_pointer_chain("Player::Instance", [0])
            if not instance_ptr:
                return False
            return self.memory.read_bool(instance_ptr + 0x188)
        except:
            return False
