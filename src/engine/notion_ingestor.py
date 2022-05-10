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

    for b in data['results']:
        content = ""
        body_type = b['type']
        if 'rich_text' in b[body_type].keys():
            if len(b[body_type]['rich_text'])==0: 
                content+="내용 없음"
            
            else: 
                sub_contents = ""
                for j in b[body_type]['rich_text']:
                    sub_contents += j['plain_text']
                content += sub_contents
        else:
            content += "내용 없음"
        
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
    
    df = pd.DataFrame()
    for i in data['results']:
        basic_content = {}
        title = ""
        for t in i['properties']['제목']['title']:
            title += t['plain_text']
        url = str(i['url'])
        address = i['id']
        contents = get_body_content(address)
        
        type_list = ""
        for ty in i['properties']['유형']['multi_select']:
            type_list += ty['name']+ ' ' 
        
        creator = i['properties']['작성자']['created_by']['name']
        hash_tags = ""
        for h in i['properties']['Hash tag']['multi_select']:
            hash_tags += h['name']+ ' '
        
        created_time = i['properties']['작성일자']['created_time']

        basic_content['subject']= title
        basic_content['description']= contents
        basic_content['content_type']= type_list
        basic_content['write_user']= creator
        basic_content['hash_tag']= hash_tags
        basic_content['created_on']= created_time
        basic_content['url'] = url
        result = pd.DataFrame([basic_content])
        df = pd.concat([df,result])
    

    # if data['has_more']:
    #     # body = json.dumps()
    #     response = requests.request("POST", url, headers=headers, data= json.dumps({"start_cursor": data['next_cursor']}))
    #     data = response.json()
    #     print(data)
    #     for i in data['results']:
    #         basic_content = {}
    #         title = ""
    #         for t in i['properties']['제목']['title']:
    #             title += t['plain_text']
    #         url = str(i['url'])
    #         address = i['id']
    #         contents = get_body_content(address)
            
    #         type_list = ""
    #         for ty in i['properties']['유형']['multi_select']:
    #             type_list += ty['name']+ ' ' 
            
    #         creator = i['properties']['작성자']['created_by']['name']
    #         hash_tags = ""
    #         for h in i['properties']['Hash tag']['multi_select']:
    #             hash_tags += h['name']+ ' '
            
    #         created_time = i['properties']['작성일자']['created_time']

    #         basic_content['subject']= title
    #         basic_content['description']= contents
    #         basic_content['content_type']= type_list
    #         basic_content['write_user']= creator
    #         basic_content['hash_tag']= hash_tags
    #         basic_content['created_on']= created_time

    #         result = pd.DataFrame([basic_content])
    #         df = pd.concat([df,result])
    # else:
    #     for i in data['results']:
    #         basic_content = {}
    #         title = ""
    #         for t in i['properties']['제목']['title']:
    #             title += t['plain_text']
            
    #         address = i['id']
    #         contents = get_body_content(address)
            
    #         type_list = ""
    #         for ty in i['properties']['유형']['multi_select']:
    #             type_list += ty['name']+ ' ' 
            
    #         creator = i['properties']['작성자']['created_by']['name']
    #         hash_tags = ""
    #         for h in i['properties']['Hash tag']['multi_select']:
    #             hash_tags += h['name']+ ' '
            
    #         created_time = i['properties']['작성일자']['created_time']

    #         basic_content['subject']= title
    #         basic_content['description']= contents
    #         basic_content['content_type']= type_list
    #         basic_content['write_user']= creator
    #         basic_content['hash_tag']= hash_tags
    #         basic_content['created_on']= created_time
    #         basic_content['url'] = url

    #         result = pd.DataFrame([basic_content])
    #         df = pd.concat([df,result])
    # df['id'] = [i for i in range(len(df))]
    return df

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
        "_id": getUniqueIndexId(str(x[1])),
        "_source": {
            "id": x[0],
            "subject": x[1],
            "description": x[2],
            "content_type": x[3],
            "write_user": x[4],
            "hash_tag": x[5],
            "created_on": x[6],
            "url":x[7]}
    }
        for x in zip(df['id'], df['subject'], df['description'], df['content_type'], df['write_user'], df['hash_tag'], df['created_on'],df['url'])
    ]
    helpers.bulk(es, data,raise_on_error=False)

def begin_ningestor():
    p = getIssues()
    issueToElasticSearch(p)
