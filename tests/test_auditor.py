import unittest
import uuid
from . import general_configurations
from llch_logger import Logger
import time
import datetime


class TestLogger(unittest.TestCase):
    l = Logger(config_file="tests/config.ini")
    general_configurations.remove_raw_files(l.config.log_folder)

    def test_a_singleton(self):
        logger1 = Logger()
        logger2 = Logger()
        self.assertTrue(logger1 == logger2)

    def test_b_send_debug(self):
        logger = Logger()
        logger.debug(f"Sending a message: DEBUG - {uuid.uuid1()}")

    def test_b_send_info(self):
        logger = Logger()
        logger.info(f"Sending a message: INFO - {uuid.uuid1()}")

    def test_b_send_warn(self):
        logger = Logger()
        logger.warn(f"Sending a message: WARN - {uuid.uuid1()}")

    def test_b_send_error(self):
        logger = Logger()
        logger.error(f"Sending a message: ERROR - {uuid.uuid1()}")

    def test_b_send_audit(self):
        logger = Logger()
        logger.audit(f"Sending a message: AUDIT - {uuid.uuid1()}")

    def test_b_send_raw(self):
        logger = Logger()
        for i in range(70):
            logger.raw(
                f"Sending a message: RAW {i} - {datetime.datetime.now()} - {uuid.uuid1()}"
            )
            time.sleep(1)

    def test_c_execution_metadata(self):
        logger = Logger()
        logger.set_execution_metadata({"metadata1": "metadata1", "metadata2": 2})
        logger.set_execution_metadata(
            {"metadata2": 22, "metadata3": "", "metadata4": None}
        )
        logger.set_execution_metadata(
            {"metadata5": {"metametadata1": "", "metametadata2": None}}
        )
        logger.info(f"Sending a message: INFO WITH EXECUTION METADATA - {uuid.uuid1()}")
        logger.unset_execution_metadata()


if __name__ == "__main__":
    unittest.main()
