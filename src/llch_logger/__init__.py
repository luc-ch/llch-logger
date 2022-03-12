import datetime
import inspect
import logging
import os
import uuid

from pythonjsonlogger import jsonlogger

from .configuration import Configuration

from ._version import __version__
from .util.singleton_meta import SingletonMeta


class Logger(metaclass=SingletonMeta):
    """Sends audit/logging messages to file

    Raises:
        IOError: Can't create logs.

    Returns:
        None: None
    """

    AUDIT_LEVEL_NUM = 5
    RAW_LEVEL_NUM = 5

    def __init__(self, app_name=None, app_version=None, config_file="config.ini"):
        super().__init__()

        self.config = Configuration(config_file)

        frame_info = inspect.stack()[len(inspect.stack()) - 4]
        main_module = inspect.getmodule(frame_info[0])
        if not hasattr(main_module, "__version__"):
            frame_info = inspect.stack()[len(inspect.stack()) - 5]
            main_module = inspect.getmodule(frame_info[0])
        if main_module.__name__ == "coverage.cmdline":
            app_name = __name__
            app_version = __version__

        self.app_name = app_name if app_name is not None else main_module.__name__
        if app_version is not None:
            self.version = app_version
        elif hasattr(main_module, "__version__"):
            self.version = main_module.__version__
        else:
            self.version = __version__

        self.process_id = str(uuid.uuid4())
        self.execution_metadata = {}
        (
            self.log_logger,
            self.audit_logger,
            self.raw_logger,
            self.stream_logger,
        ) = self._create_all_loggers()

    def set_execution_metadata(self, execution_metadata: dict):
        if not isinstance(execution_metadata, dict):
            raise ValueError(
                f"Tipo de dato incorrecto: Usado {format(type(execution_metadata))} en vez de dict."
            )
        if len(self.execution_metadata) > 0:
            self.execution_metadata.update(execution_metadata)
        else:
            self.execution_metadata = execution_metadata

    def unset_execution_metadata(self):
        self.execution_metadata = {}

    def debug(self, msg, extra=None):
        self._log(logging.DEBUG, msg, extra)

    def info(self, msg, extra=None):
        self._log(logging.INFO, msg, extra)

    def warn(self, msg, extra=None):
        self._log(logging.WARN, msg, extra)

    def error(self, msg, extra=None):
        self._log(logging.ERROR, msg, extra)

    def audit(self, msg, extra=None):
        log = self._create_base_log(msg, extra)
        self.audit_logger.log(Logger.AUDIT_LEVEL_NUM, log)

    def raw(self, msg):
        self.raw_logger.log(Logger.RAW_LEVEL_NUM, msg)

    def _log(self, level, msg, extra=None):
        log = self._create_base_log(msg, extra)
        log["type"] = logging.getLevelName(level)
        self.stream_logger.log(level, msg)
        self.log_logger.log(level, log)

    def _create_base_log(self, msg, extra=None):
        log = {}
        log["message"] = msg
        log["eventId"] = str(uuid.uuid4())
        log["eventDate"] = (
            datetime.datetime.utcnow()
            .replace(tzinfo=datetime.timezone.utc)
            .astimezone()
            .isoformat()
        )
        log["correlationId"] = self.process_id
        log["header"] = {}
        log["header"]["source"] = {}
        log["header"]["source"]["version"] = self.version
        log["header"]["source"]["appName"] = self.app_name
        log["header"]["host"] = {}
        log["header"]["host"]["name"] = self.config.hostname
        log["header"]["host"]["ip"] = self.config.container_ip
        log["payload"] = {}
        log["payload"]["message"] = msg
        if len(self.execution_metadata) > 0 or isinstance(extra, dict):
            log["payload"]["additionalFields"] = {}
            if len(self.execution_metadata) > 0:
                log["payload"]["additionalFields"].update(self.execution_metadata)
            if isinstance(extra, dict):
                log["payload"]["additionalFields"].update(extra)
        return log

    def _create_audit_logger(self, json_formatter):
        logging.addLevelName(Logger.AUDIT_LEVEL_NUM, "AUDIT")

        def audit(self, message, *args, **kws):
            if self.isEnabledFor(Logger.AUDIT_LEVEL_NUM):
                self._log(Logger.AUDIT_LEVEL_NUM, message, args, **kws)

        audit_logger = logging.getLogger("Audit")
        audit_logger.setLevel(Logger.AUDIT_LEVEL_NUM)
        audit_logger.audit = audit
        audit_handler = logging.FileHandler(
            os.path.join(self.config.log_folder, f"audit-{self.app_name}.log"),
            encoding="utf-8",
        )
        audit_handler.setFormatter(json_formatter)
        audit_logger.addHandler(audit_handler)
        return audit_logger

    def _create_basic_logger(self, json_formatter):
        log_logger = logging.getLogger("Log")
        log_logger.setLevel(logging.getLevelName(self.config.log_level.upper()))
        log_handler = logging.FileHandler(
            os.path.join(self.config.log_folder, f"log-{self.app_name}.log"),
            encoding="utf-8",
        )
        log_handler.setFormatter(json_formatter)
        log_logger.addHandler(log_handler)
        return log_logger

    def _create_raw_logger(self):
        def raw(self, message, *args, **kws):
            if self.isEnabledFor(Logger.RAW_LEVEL_NUM):
                self._log(Logger.RAW_LEVEL_NUM, message, args, **kws)

        raw_logger = logging.getLogger("Raw")
        raw_logger.setLevel(Logger.RAW_LEVEL_NUM)
        raw_logger.raw = raw
        raw_handler = logging.FileHandler(
            os.path.join(self.config.log_folder, f"raw-{self.app_name}.txt"),
            encoding="utf-8",
        )
        raw_handler.setFormatter(logging.Formatter("%(message)s"))
        raw_logger.addHandler(raw_handler)
        return raw_logger

    def _create_stream_logger(self):
        stream_logger = logging.getLogger("Console")
        if self.config.write_to_stdout:
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(
                logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")
            )
            stream_logger.addHandler(stream_handler)
        return stream_logger

    def _create_all_loggers(self,):
        try:
            os.makedirs(self.config.log_folder, exist_ok=True)
        except Exception as e:
            raise IOError(
                f"Error al crear los loggers en {self.config.log_folder}. Chequear permisos."
            ) from e

        json_formatter = jsonlogger.JsonFormatter()

        logging.basicConfig(level=logging.NOTSET, handlers=[])

        basic_logger = self._create_basic_logger(json_formatter)
        audit_logger = self._create_audit_logger(json_formatter)
        raw_logger = self._create_raw_logger()
        stream_logger = self._create_stream_logger()

        return basic_logger, audit_logger, raw_logger, stream_logger
