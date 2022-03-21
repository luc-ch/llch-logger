import unittest

from llch_logger import Logger

import multiprocessing

# Multithreading only works on Linux and MacOS (Windows is built differently and can't lock singletons the same way)


def spawn(num):
    mylogger = Logger()
    mylogger.debug(f"Sending a message: {num}")


class TestMultithreading(unittest.TestCase):
    def test_b_send_info(self):
        Logger()
        for i in range(25):
            p = multiprocessing.Process(target=spawn, args=(i,))
            p.start()


if __name__ == "__main__":
    unittest.main()
