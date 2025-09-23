from . import Base

class AudioEngine(Base):
    def __init__(self):
        super().__init__()

    @property
    def time(self) -> int:
        try:
            # [[AudioEngine::Time] + 0] + 0
            time_offset = self.memory.offsets.get("AudioEngine::Time")
            if not time_offset:
                return 0
            # [[AudioEngine::Time] + 0] + 0
            time_ptr = self.memory.read_int(time_offset)
            if not time_ptr:
                return 0
            # [[AudioEngine::Time] + 0] + 0
            return self.memory.read_int(time_ptr)
        except:
            return 0
