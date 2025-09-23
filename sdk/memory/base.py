class Base:
    """
    Base class that provides persistent memory access to all SDK classes.
    """
    
    def __init__(self):
        """Initialize the base class with memory access"""
        # Import here to avoid circular import
        from .memory import Memory
        self._memory = Memory.get_instance()
    
    @property
    def memory(self):
        """Get the memory instance"""
        return self._memory