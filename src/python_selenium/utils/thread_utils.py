import concurrent.futures
import time
from datetime import timedelta

COMMON_EXECUTOR = concurrent.futures.ThreadPoolExecutor()


def sleep_for(duration: timedelta):
    time.sleep(duration.total_seconds())
