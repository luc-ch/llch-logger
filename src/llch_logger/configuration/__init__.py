import configparser
import os
import socket

from ..util import import_data


class Configuration:
    """
    Loads the default configurations for the program to work properly
    """

    def __init__(self, config_file_path="config.ini", default_file_path="default.ini"):
        config_parser = self._read_config_file(config_file_path, default_file_path)
        self._setup_variables(config_parser)

    def _read_config_file(
        self, config_file_path="config.ini", default_file_path="default.ini"
    ):
        import_data.copy_config_to_cwd()
        config_parser = configparser.ConfigParser()
        config_parser.read(default_file_path)
        config_parser.read(config_file_path)
        return config_parser

    def _setup_variables(self, config_parser):
        self.log_level = config_parser.get("log", "log_level")
        self.log_folder = config_parser.get("log", "log_folder")
        self.write_to_stdout = config_parser.getboolean("log", "write_to_stdout")
        self.hostname = socket.gethostname()
        self.external_ip = os.environ.get("ADDRESS_EXTERNAL")
        self.internal_ip = socket.gethostbyname(self.hostname)
        self.container_ip = (
            self.internal_ip
            if self.external_ip is None
            else f"{self.external_ip},{self.internal_ip}"
        )
