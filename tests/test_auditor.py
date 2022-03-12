import unittest

from llch_logger import Logger


class TestLogger(unittest.TestCase):
    def test_a_singleton(self):
        logger1 = Logger()
        logger2 = Logger()
        self.assertTrue(logger1 == logger2)

    def test_b_send_debug(self):
        logger = Logger()
        logger.debug("Sending a message: DEBUG")

    def test_b_send_info(self):
        logger = Logger()
        logger.info("Sending a message: INFO")

    def test_b_send_warn(self):
        logger = Logger()
        logger.warn("Sending a message: WARN")

    def test_b_send_error(self):
        logger = Logger()
        logger.error("Sending a message: ERROR")

    def test_b_send_audit(self):
        logger = Logger()
        logger.audit("Sending a message: AUDIT")

    def test_b_send_raw(self):
        logger = Logger()
        logger.raw("Sending a message: RAW")

    def test_c_execution_metadata(self):
        logger = Logger()
        logger.set_execution_metadata({"metadata1": "metadata1", "metadata2": 2})
        logger.set_execution_metadata(
            {"metadata2": 22, "metadata3": "", "metadata4": None}
        )
        logger.info("Sending a message: INFO WITH EXECUTION METADATA")
        logger.unset_execution_metadata()


if __name__ == "__main__":
    unittest.main()
