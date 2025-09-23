import json
import pymem
import ctypes
import re
from ctypes import wintypes

PAGE_READONLY = 0x02
PAGE_READWRITE = 0x04
PAGE_EXECUTE_READ = 0x20
PAGE_EXECUTE_READWRITE = 0x40
MEM_COMMIT = 0x1000

class MEMORY_BASIC_INFORMATION(ctypes.Structure):
    _fields_ = [
        ('BaseAddress', ctypes.c_void_p),
        ('AllocationBase', ctypes.c_void_p),
        ('AllocationProtect', wintypes.DWORD),
        ('RegionSize', ctypes.c_size_t),
        ('State', wintypes.DWORD),
        ('Protect', wintypes.DWORD),
        ('Type', wintypes.DWORD),
    ]

# --- Pattern helpers ---
def parse_pattern(pattern_str):
    """Helper function to parse a pattern"""
    parts = pattern_str.split()
    pattern_bytes = bytearray()
    mask = ''
    for part in parts:
        if part in ('?', '??'):
            pattern_bytes.append(0x00)
            mask += '?'
        else:
            pattern_bytes.append(int(part, 16))
            mask += 'x'
    return bytes(pattern_bytes), mask

def pattern_to_regex(pattern: bytes, mask: str) -> bytes:
    """Helper function to convert a pattern to a regex"""
    regex = b''
    for i in range(len(pattern)):
        regex += re.escape(pattern[i:i+1]) if mask[i] == 'x' else b'.'
    return regex

def scan_process_memory(pm, pattern_bytes, mask):
    """Helper function to scan for signatures in the process memory"""
    mbi = MEMORY_BASIC_INFORMATION()
    address = 0
    max_address = 0x7FFFFFFF_FFFF if ctypes.sizeof(ctypes.c_void_p) == 8 else 0x7FFFFFFF

    pattern_re = re.compile(pattern_to_regex(pattern_bytes, mask), flags=re.DOTALL)
    readable = [PAGE_READONLY, PAGE_READWRITE, PAGE_EXECUTE_READ, PAGE_EXECUTE_READWRITE]

    while address < max_address and ctypes.windll.kernel32.VirtualQueryEx(
        pm.process_handle, ctypes.c_void_p(address),
        ctypes.byref(mbi), ctypes.sizeof(mbi)
    ):
        if mbi.State == MEM_COMMIT and mbi.Protect in readable:
            try:
                chunk = pm.read_bytes(mbi.BaseAddress, mbi.RegionSize)
            except Exception:
                address += mbi.RegionSize
                continue

            match = pattern_re.search(chunk)
            if match:
                return mbi.BaseAddress + match.start()

        address += mbi.RegionSize
    return None

class Memory:
    """
    Memory class for reading and scanning process memory of osu!.
    
    This class implements a singleton pattern to ensure only one instance exists
    and provides persistent memory access across all SDK classes.

    This class provides:
    - Signature scanning using patterns defined in a JSON file (default: "signatures.json").
    - Storage of resolved memory addresses for each signature.
    - Low-level helpers for reading integers, booleans, and C#-style strings from process memory.

    Attributes:
        pm: pymem.Pymem instance for process memory access.
        sigs: List of signature definitions loaded from the JSON file.
        offsets: Dictionary mapping signature names to resolved memory addresses.

    Methods:
        __init__(sig_file="signatures.json"):
            Initializes the Memory object, loads signatures, and scans for their addresses.
        _scan_signatures():
            Scans the process memory for all signatures and stores their addresses.
        read_int(address: int) -> int:
            Reads a 4-byte integer from the specified address.
        read_bool(address: int) -> bool:
            Reads a boolean value from the specified address.
        read_csharp_string32(address: int, max_len: int = 4096) -> str:
            Reads a C#-style UTF-16 string from the specified address.
        get_instance(sig_file="signatures.json") -> Memory:
            Class method to get the singleton instance.
    """
    _instance = None
    _initialized = False
    
    def __new__(cls, sig_file="signatures.json"):
        """Ensure only one instance exists (singleton pattern)"""
        if cls._instance is None:
            cls._instance = super(Memory, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, sig_file="signatures.json"):
        """Initialize the Memory class (only once due to singleton)"""
        if Memory._initialized:
            return
            
        self.pm = pymem.Pymem("osu!.exe")

        with open(sig_file, "r") as f:
            self.sigs = json.load(f)["signatures"]

        self.offsets = {}
        self._scan_signatures()
        Memory._initialized = True
    
    @classmethod
    def get_instance(cls, sig_file="signatures.json"):
        """Get the singleton instance of Memory"""
        if cls._instance is None:
            cls._instance = cls(sig_file)
        return cls._instance
    

    def _scan_signatures(self):
        """Scan for signatures in the process memory"""
        module = pymem.process.module_from_name(self.pm.process_handle, "osu!.exe")
        module_base = module.lpBaseOfDll

        for sig in self.sigs:
            pattern_bytes, mask = parse_pattern(sig["pattern"])
            addr = scan_process_memory(self.pm, pattern_bytes, mask)

            if addr is None:
                self.offsets[sig["name"]] = None
                continue

            if sig.get("rva", False):
                addr = module_base + (addr - module_base)

            addr += sig["offset"]
            self.offsets[sig["name"]] = addr

    def read_int(self, address: int) -> int:
        """Read an integer from the given address"""
        try:
            return self.pm.read_int(address)
        except:
            return 0

    def read_short(self, address: int) -> int:
        """Read a short from the given address"""
        try:
            return self.pm.read_short(address)
        except:
            return 0

    def read_double(self, address: int) -> float:
        """Read a double from the given address"""
        try:
            return self.pm.read_double(address)
        except:
            return 0.0
    
    def read_float(self, address: int) -> float:
        """Read a float from the given address"""
        try:
            return self.pm.read_float(address)
        except:
            return 0.0

    def read_bool(self, address: int) -> bool:
        """Read a boolean from the given address"""
        try:
            return self.pm.read_bool(address)
        except:
            return False

    def read_csharp_string32(self, address: int, max_len: int = 4096) -> str:
        """Read a C# string from the given address"""
        if not address or address < 0x10000:
            return ""
        try:
            length = self.pm.read_int(address + 0x4)
            if length <= 0 or length > max_len:
                return ""
            raw = self.pm.read_bytes(address + 0x8, length * 2)
            return raw.decode("utf-16-le", errors="ignore")
        except Exception:
            return ""

    def resolve_pointer_chain(self, base_offset_name: str, chain: list) -> int:
        """
        Resolve a pointer chain dynamically from memory.
        
        Args:
            base_offset_name: Name of the base offset in signatures (e.g., "Rulesets")
            chain: List of offsets to follow (e.g., [-0xb, 0x4, 0x68, 0x38])
        
        Returns:
            Final resolved address, or 0 if chain fails
        """
        try:
            base_offset = self.offsets.get(base_offset_name)
            if not base_offset:
                return 0
                
            current_addr = base_offset
            
            for offset in chain:
                if current_addr < 0x1000:
                    return 0
                current_addr = self.read_int(current_addr + offset)
                
            return current_addr if current_addr > 0x1000 else 0
        except Exception:
            return 0