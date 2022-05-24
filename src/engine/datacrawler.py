from engine.create_rindex import create_rm_index
from engine.create_pindex import create_pt_index
from engine.create_nindex import create_nt_index
from engine.redmine_ingestor import begin_ringestor
from engine.portal_ingestor import begin_pingestor
from engine.notion_ingestor import begin_ningestor
from engine.create_rspindex import create_rsp_index
from engine.redminesp_ingestor import begin_rspingestor

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
addWorker(id=CreateNotionIndex,
          func=create_nt_index)
addWorker(id=CreateRedminespIndex,
          func=create_rsp_index)

addWorker(id=IngestRedmineData,
          func=begin_ringestor)
addWorker(id=IngestPortalData,
          func=begin_pingestor)
addWorker(id=IngestNotionData,
          func=begin_ningestor)
addWorker(id=IngestRedminespData,
          func=begin_rspingestor)