import datetime
import hashlib
import json
import requests
import pymysql 
from util.querystore import *
from datetime import datetime

REDMINE_DB_PORT = 330
REDMINE_DB_DATABASE = 'redmine'
REDMINE_DB_USER = "root"
REDMINE_DB_PASSWORD = "root!"
REDMINE_DB_HOST ='localhost'

def get_conn():
    conn = pymysql.connect(host=REDMINE_DB_HOST,port=REDMINE_DB_PORT,user=REDMINE_DB_USER,passwd=REDMINE_DB_PASSWORD,db=REDMINE_DB_DATABASE,charset='utf8')
    return conn

# SQL 에 연결하여 이슈 테이블을 추출하여 ProductIssue list 로 돌려주는 함수입니다
def getIssues():
    cnx = get_conn()
    cursor = cnx.cursor()
    query = redmine_common_query_list['issues_d']
    # query = ('SELECT posts.ID AS id, posts.post_content AS content, posts.post_title AS title, posts.guid AS post_url, posts.post_date AS post_date, posts.post_modified AS modified_date, metadata.meta_value AS meta_value, image_data.meta_value AS image FROM wp_posts AS posts JOIN wp_postmeta AS image_metadata ON image_metadata.post_id = posts.ID JOIN wp_postmeta AS image_data ON image_data.post_id = image_metadata.meta_value JOIN wp_postmeta AS metadata ON metadata.post_id = posts.ID WHERE posts.post_status = "publish" AND posts.post_type = "product" AND metadata.meta_key = "_product_attributes" AND image_metadata.meta_key = "_thumbnail_id" AND image_data.meta_key = "_wp_attached_file"')
    cursor.execute(query)

    issue_list = []
    for (id, description, tracker_id, project_id, status_id, subject, created_on, updated_on) in cursor:
        print("Issue id {} found. created on: {}".format(id,created_on))
        issue = ProductIssue(id, description,tracker_id, project_id, status_id, subject, created_on, updated_on)
        issue_list.append(issue)

    cursor.close()
    cnx.close()
    return issue_list

# 엘라스틱서치에 출력하는 함수입니다. 
def issueToElasticSearch(issues):
    putUrlPrefix = 'http://localhost:9200/issues/_doc/'
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    for issue in issues:
        id = getUniqueIndexId(issue.subject)
        # print(id)
        r = requests.put(putUrlPrefix + id, data=json.dumps(issue.__dict__,indent=4, sort_keys=True, default=json_field_handler), headers=headers)
        # print(r.json())
        if r.status_code >= 400:
           print("There is an error writing to elasticsearch")
           print(r.status_code)
           print(r.json())

# Custom handlers for marshalling python object into JSON 
def json_field_handler(x):
    if isinstance(x, datetime):
        return x.isoformat()
    raise TypeError("Unable to parse json field")

# 엘라스틱서치에서 사용될 문서의 고유 아이디를 생성합니다.
def getUniqueIndexId(pri):
    return hashlib.sha1(pri.encode('utf-8')).hexdigest()

# 이슈를 표현하는 class 입니다.
class ProductIssue(object):
  """
    Represents semantic data for a single product post
  """
  def __init__(self, id, description, tracker_id, project_id, status_id, subject, created_on, updated_on):
    self.id = id
    self.description = description
    self.tracker_id = tracker_id
    self.project_id = project_id
    self.status_id = status_id
    self.subject = subject
    self.created_on= created_on
    self.updated_on = updated_on



p = getIssues()
issueToElasticSearch(p)
