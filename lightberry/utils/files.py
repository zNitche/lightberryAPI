import os


def file_exists(path):
    try:
        os.stat(path)

        return True
    except OSError:
        return False
