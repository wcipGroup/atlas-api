import os
import json

class Configuration:

    __cfg = None

    def __init__(self, file_path):

        if Configuration.__cfg:
            raise SystemExit("Configuration already defined!")

        if not file_path:
            raise SystemExit("Configuration file not found")

        self.__cfg = self.__parse(file_path)

        Configuration.__cfg = self.__cfg

    @staticmethod
    def __parse(file_path):
        if not os.path.isfile(file_path):
            raise SystemExit("Configuration file {0} is missing".format(file_path))

        try:
            with open(file_path) as f:
                return json.loads(f.read())
        except Exception as e:
            exception = str(e)

        raise SystemExit("Configuration file {0} exception: {1}".format(file_path, exception))

    @staticmethod
    def get():
        if Configuration.__cfg:
            return Configuration.__cfg

        raise SystemExit("Configuration is not set")