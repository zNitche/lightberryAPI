import os


def file_exists(path: str) -> bool:
    if not path:
        return False

    try:
        os.stat(path)

        return True
    except OSError:
        return False


def get_free_space() -> float:
    stat = os.statvfs("/")
    free = stat[0] * stat[3]

    return free / 1024


def get_file_size(file_path: str) -> float:
    return os.stat(file_path)[6] if file_exists(file_path) else 0
