from engine.datacrawler import workers
from logger.logger import root_logger
from engine.jobq import popJob
import threading
import logging
import time

def worker(id):
    root_logger.info("Start Worker " + id)
    while True:
        try:
            job = popJob()  # A work starts here
            if job is None:
                time.sleep(1)
                continue
            root_logger.info("Pop Job  " + job)
            worker = workers[job]
            if worker is None:
                root_logger.warning("Cannot find [" + job + "]")
                continue

            worker_function = worker.func
            worker_function()  # Run function

            root_logger.info("Done Job  " + job)

        except Exception as e:
            logging.exception('exc_info', exc_info=e)
            root_logger.info("Worker Exception")

def startWorker():
    th = threading.Thread(target=worker,
                          name="[th def {}]".format("1"),
                          args=("1"))
    th.start()
