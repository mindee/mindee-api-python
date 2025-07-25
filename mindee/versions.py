import sys

__version__ = "4.25.0"

PYTHON_VERSION = f"{sys.version_info[0]}.{sys.version_info[1]}"


def get_platform() -> str:
    """Get the current OS platform."""
    platforms = {
        "linux": "linux",
        "win32": "windows",
        "darwin": "macos",
        "aix": "aix",
        "freebsd": "bsd",
        "openbsd": "bsd",
    }
    for name, agent_name in platforms.items():
        if sys.platform.startswith(name):
            return agent_name
    return sys.platform
