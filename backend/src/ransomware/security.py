import platform
import sys


def is_being_debugged() -> bool:
    if sys.gettrace() is not None:
        return True
    if platform.system() == "Windows":
        try:
            import ctypes

            return bool(ctypes.windll.kernel32.IsDebuggerPresent())
        except Exception:
            return False
    return False
