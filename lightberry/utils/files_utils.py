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
