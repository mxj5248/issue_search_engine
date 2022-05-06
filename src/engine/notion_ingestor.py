import requests
import json
import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import hashlib

# 이슈를 표현하는 class 입니다.
class ProductIssue(object):
  """
    Represents semantic data for a single product post
  """
  def __init__(self, subject, description, content_type, write_user, hash_tag, created_on):
    self.subject = subject
    self.description = description
    self.content_type = content_type
    self.write_user = write_user
    self.hash_tag = hash_tag
    self.created_on= created_on

def get_body_content(address):
    url = "https://api.notion.com/v1/blocks/"+address+"/children"
    payload = json.dumps({
    })
    headers = {
        'Authorization': 'Bearer secret_lrHfKHS6SaaMVkNVlISGpMxROOxeHHsoQH1z4mgZmmr',
        'Notion-Version': '2022-02-22'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()

    body_type = data['results'][0]['type']
    if 'rich_text' in data['results'][0][body_type].keys():
        if len(data['results'][0][body_type]['rich_text'])==0: 
            content="내용없음"
            return content
        else: content = data['results'][0][body_type]['rich_text'][0]['plain_text']
        return content
    else:
        content = "내용없음"
        return content

# 엘라스틱서치에서 사용될 문서의 고유 아이디를 생성합니다.
def getUniqueIndexId(pri):
    return hashlib.sha1(pri.encode('utf-8')).hexdigest()

# SQL 에 연결하여 이슈 테이블을 추출하여 ProductIssue list 로 돌려주는 함수입니다
def getIssues():
    url = "https://api.notion.com/v1/databases/d22323a20ddc41d2b89a3d4990442309/query"
    payload = json.dumps({
    })
    headers = {
        'Authorization': 'Bearer secret_lrHfKHS6SaaMVkNVlISGpMxROOxeHHsoQH1z4mgZmmr',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-02-22'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    data = response.json()
    result = pd.DataFrame(data['results'])
    contents = [get_body_content(address)for address in list(pd.DataFrame(data['results'])['id'])]
    result['content'] = contents
    result = result[['title','content','content_type','writer_user','hash_tag','created_on']]
    result.rename(columns={'title':'subject','content':'description'},inplace=True)
    return result

# 엘라스틱서치에 출력하는 함수입니다. 
def issueToElasticSearch(df):
    url = "http://elasticsearch"
    port = "9200"

    def get_conn():
        es = Elasticsearch(f'{url}:{port}')
        return es
    es = get_conn()
    data = [
    {
        "_index": "notion",
        "_type": "_doc",
        "_id": getUniqueIndexId(str(x[0])),
        "_source": {
            "subject": x[0],
            "description": x[1],
            "content_type": x[2],
            "writer_user": x[3],
            "hash_tag": x[4],
            "created_on": x[5]}
    }
        for x in zip(df['subject'], df['description'], df['content_type'], df['writer_user'], df['hash_tag'], df['created_on'])
    ]
    helpers.bulk(es, data,raise_on_error=False)

def begin_ningestor():
    p = getIssues()
    issueToElasticSearch(p)