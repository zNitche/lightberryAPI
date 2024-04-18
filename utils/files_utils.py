import os


def file_exists(path):
    try:
        os.stat(path)

        return True
    except OSError:
        return False


def get_free_space():
    stat = os.statvfs("/")
    free = stat[0] * stat[3]

    return free / 1024


def get_file_size(file_path):
    return os.stat(file_path)[6] if file_exists(file_path) else 0
