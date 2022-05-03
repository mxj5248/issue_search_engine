# Multi thread 환경에서 queue가 보호되지 않을 수 있으니 single thread 사용을 권장 합니다.
from queue import Queue

q = Queue()
def remainingJob():
    return q.size()
def popJob():
    return q.get()
def pushJob(job):
    q.put(job)
def clearJob():
    q.queue.clear()