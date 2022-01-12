import sys

__version__ = "1.2.3"

python_version = "%s.%s" % (sys.version_info[0], sys.version_info[1])


def get_platform() -> str:
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
