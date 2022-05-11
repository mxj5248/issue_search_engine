from util.querystore import *
from datetime import datetime
import datetime
import hashlib
import json
import requests
import pymysql 
import os
from pymysqlpool.pool import Pool
from abc import *
import pandas as pd
import time
from elasticsearch import Elasticsearch
from elasticsearch import helpers
# 이슈를 표현하는 class 입니다.
class ProductIssue(object):
  """
    Represents semantic data for a single product post
  """
  def __init__(self, id, description, tracker_id, project_id, status_id, subject, created_on, updated_on,assigned_to_id):
    self.id = id
    self.description = description
    self.tracker_id = tracker_id
    self.project_id = project_id
    self.status_id = status_id
    self.subject = subject
    self.created_on= created_on
    self.updated_on = updated_on
    self.assigned_to_id = assigned_to_id

REDMINE_DB_PORT = int(os.getenv("REDMINE_DB_PORT"))
REDMINE_DB_DATABASE = os.getenv("REDMINE_DB_DATABASE")
REDMINE_DB_USER = os.getenv("REDMINE_DB_USER")
REDMINE_DB_PASSWORD = os.getenv("REDMINE_DB_PASSWORD")
REDMINE_DB_HOST = os.getenv("REDMINE_DB_HOST")

def get_conn():
    conn = pymysql.connect(host=REDMINE_DB_HOST,port=REDMINE_DB_PORT,user=REDMINE_DB_USER,passwd=REDMINE_DB_PASSWORD,db=REDMINE_DB_DATABASE,charset='utf8')
    return conn

#// Pool에 Connection 반환 ( 무조건 해 주어야 한다. )
def release(conn):
    conn.close()

def json_default(value): 
    if isinstance(value, datetime.date): 
        return value.strftime('%Y-%m-%d') 
    raise TypeError('not JSON serializable')

# Custom handlers for marshalling python object into JSON 
def json_field_handler(x):
    if isinstance(x, datetime):
        return x.isoformat()
    raise TypeError("Unable to parse json field")

# 엘라스틱서치에서 사용될 문서의 고유 아이디를 생성합니다.
def getUniqueIndexId(pri):
    return hashlib.sha1(pri.encode('utf-8')).hexdigest()

# SQL 에 연결하여 이슈 테이블을 추출하여 ProductIssue list 로 돌려주는 함수입니다
def getIssues():
    conn = get_conn()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    # query = redmine_common_query_list['issues_d'] 
    query = "SELECT id, description, tracker_id, project_id, status_id, subject, created_on, updated_on, assigned_to_id FROM redmine.issues i WHERE i.created_on >= '2020-01-01' AND i.project_id in (77,79)"
    cursor.execute(query)
    data = cursor.fetchall()
    result = pd.DataFrame(data,columns=['id', 'description', 'tracker_id', 'project_id', 'status_id', 'subject', 'created_on', 'updated_on','assigned_to_id'])
    issue_list = []
    for row, value in result.iterrows():
        print("Issue id {} found. created on: {}".format(value['id'],value['created_on']))
        issue = ProductIssue(value['id'], value['description'], value['tracker_id'], value['project_id'],value['status_id'], value['subject'], value['created_on'], value['updated_on'],value['assigned_to_id'])
        issue_list.append(issue)


    # for (id, description, tracker_id, project_id, status_id, subject, created_on, updated_on) in cursor:
    #     print("Issue id {} found. created on: {}".format(id,created_on))
    #     issue = ProductIssue(id, description,tracker_id, project_id, status_id, subject, created_on, updated_on)
    #     issue_list.append(issue)

    release(conn)
    # return issue_list
    return result

# 엘라스틱서치에 출력하는 함수입니다. 
def issueToElasticSearch(df):
    putUrlPrefix = 'http://localhost:9200/redmine/_doc/'
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    # es = Elasticsearch(hosts="http://elasticsearch", port=9200)
    url = "http://elasticsearch"
    port = "9200"

    def get_conn():
        es = Elasticsearch(f'{url}:{port}')
        return es
    es = get_conn()
    data = [
    {
        "_index": "idx_redmine",
        "_type": "_doc",
        "_id": getUniqueIndexId(x[5]),
        "_source": {
            "id": x[0],
            "description": x[1],
            "tracker_id": x[2],
            "project_id": x[3],
            "status_id": x[4],
            "subject": x[5],
            "created_on": x[6],
            "updated_on": x[7],
            "assigned_to_id": x[8]}
    }
        for x in zip(df['id'], df['description'], df['tracker_id'], df['project_id'],df['status_id'], df['subject'], df['created_on'], df['updated_on'],df['assigned_to_id'])
    ]
    helpers.bulk(es, data, raise_on_error=False)

    # for issue in issues:
        # id = getUniqueIndexId(issue.subject)
        # r = requests.put(putUrlPrefix + id, data=json.dumps(issue.__dict__,indent=4, sort_keys=True, default=json_default), headers=headers)
        # if r.status_code >= 400:
        #    print("There is an error writing to elasticsearch")
        #    print(r.status_code)
        #    print(r.json())


def begin_ringestor():
    p = getIssues()
    issueToElasticSearch(p)