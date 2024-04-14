from lightberry.config import Config
from lightberry import Server
from lightberry.utils import common_utils, files_utils


def main():
    common_utils.print_debug(f"Free space: {files_utils.get_free_space()} kB",
                             debug_enabled=Config.DEBUG)

    server = Server()

    server.init()
    server.start()


if __name__ == '__main__':
    main()
