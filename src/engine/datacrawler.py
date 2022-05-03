from engine.create_rindex import create_rm_index
from engine.create_pindex import create_pt_index
from engine.redmine_ingestor import begin_ringestor
from engine.portal_ingestor import begin_pingestor
from logger.logger import root_logger
from engine.jobids import *

workers = dict()

class workerWrapper:
    def __init__(self, job_id, func):
        self.job_id = job_id
        self.func = func

    def get_func(self):
        return self.func

def addWorker(id, func):
    root_logger.info("Add worker " + id)
    workers[id] = workerWrapper(id, func)

# Dashboard Worker
addWorker(id=CreateRedmineIndex,
          func=create_rm_index)
addWorker(id=CreatePortalIndex,
          func=create_pt_index)

addWorker(id=IngestRedmineData,
          func=begin_ringestor)
addWorker(id=IngestPortalData,
          func=begin_pingestor)