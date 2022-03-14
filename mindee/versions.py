import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_path, "version"), "r", encoding="utf-8") as version_file:
    __version__ = version_file.read().strip()

python_version = "%s.%s" % (sys.version_info[0], sys.version_info[1])


def get_platform() -> str:
    """Get the current OS platform."""
    platforms = {
        "linux": "linux",
        "win32": "windows",
        "darwin": "macos",
        "aix": "aix",
        "freebsd": "freebsd",
    }
    for name, agent_name in platforms.items():
        if sys.platform.startswith(name):
            return agent_name
    return sys.platform
