# from util.querystore import *
import pymysql 
import datetime
import pandas as pd
import hashlib
import json
import requests
# 이슈를 표현하는 class 입니다.
class ProductIssue(object):
  """
    Represents semantic data for a single product post
  """
  def __init__(self, id, subject, description, issue_type, site_name, biz_title, issue_manage_user, created_on):
    self.id = id
    self.subject = subject
    self.description = description
    self.issue_type = issue_type
    self.site_name = site_name
    self.biz_title = biz_title
    self.issue_manage_user = issue_manage_user
    self.created_on= created_on

PORTAL_DB_DATABASE = 'NETAND_PORTAL_V1'
PORTAL_DB_USER = "root"
PORTAL_DB_PASSWORD = "Netand141!"
PORTAL_DB_HOST ='192.168.0.50'

def get_conn():
    conn = pymysql.connect(host=PORTAL_DB_HOST,user=PORTAL_DB_USER,passwd=PORTAL_DB_PASSWORD,db=PORTAL_DB_DATABASE,charset='utf8')
    return conn
def json_default(value): 
    if isinstance(value, datetime.date): 
        return value.strftime('%Y-%m-%d') 
    raise TypeError('not JSON serializable')

# SQL 에 연결하여 이슈 테이블을 추출하여 ProductIssue list 로 돌려주는 함수입니다
def getIssues():
    cnx = get_conn()
    cursor = cnx.cursor()
    # query = redmine_common_query_list['portal_d']
    query = '''
        SELECT * FROM 
        (SELECT
        IDT.ISSUE_DATA_NUM AS issue_data_num,
        NIDT.TITLE AS title,
        F.VALUE AS content,
        IF(DIT.NAME IS NULL OR DIT.NAME = '' , DIT2.NAME, DIT.NAME) AS issue_type,
        DST.NAME AS site_name,
        DIGT.TITLE as biz_title,
        DUT.NAME AS issue_manage_user,
        IDT.REG_DT AS create_on
        FROM
        NADPORTAL_IDX_DEFAULT_TB NIDT 
        INNER JOIN ISSUE_DATA_TB IDT ON   NIDT.ISSUE_DATA_UID = IDT.UID
        INNER JOIN DEF_SITE_TB DST ON IDT.SITE_UID = DST.UID
        INNER JOIN BIZ_INFO_TB BIT ON IDT.BIZ_UID = BIT.UID
        INNER JOIN DEF_ISSUE_GROUP_TB DIGT ON DIGT.UID = BIT.ISSUE_GROUP_UID
        LEFT OUTER JOIN DEF_ISSUE_TB DIT ON IDT.ISSUE_UID = DIT.UID
        LEFT OUTER JOIN DEF_ISSUE_TB DIT2 ON IDT.ISSUE_TEMPLATE_UID = DIT2.UID
        INNER JOIN (
                SELECT * FROM (
                    SELECT 
                            DIT.UID as uid,      
                            DIT.NAME as name,
                            DIT.ISSUE_ID as issueId
                        FROM 
                            DEF_ISSUE_TB DIT LEFT OUTER JOIN DEF_ISSUE_GROUP_TB DIGT
                            ON DIT.ISSUE_GROUP_UID = DIGT.UID
                            LEFT OUTER JOIN DEF_ISSUE_TB DIT2
                            ON DIT.TEMPLATE_UID = DIT2.UID
                        WHERE
                            DIT.PARENT_UID IN (SELECT UID FROM DEF_ISSUE_TB DIT3 WHERE DIT3.NAME IN ('SR','구축'))
                            AND DIT.USE_GB = 'DATA'
                    UNION ALL 
                    SELECT 
                            UID, 
                            NAME, 
                            ISSUE_ID 
                        FROM 
                            DEF_ISSUE_TB dit4 
                        WHERE 
                            NAME IN ('SR', '라이선스', '구축')
                    ) A 
                    GROUP BY UID, NAME, ISSUEID
                ) T ON IDT.ISSUE_UID = T.UID
        LEFT OUTER JOIN DEF_USER_TB DUT ON NIDT.ISSUE_MANAGE_USER = DUT.UID 
        LEFT OUTER JOIN (
                    SELECT 
                            IFDT.ISSUE_DATA_UID, 
                            IFDT.VALUE 
                    FROM 
                        ISSUE_FIELD_DATA_TB IFDT LEFT OUTER JOIN DEF_FIELD_TB DFT ON IFDT.FIELD_UID = DFT.UID 
                    WHERE 
                        DFT.FIELD_KEY = 'CONTENT'
                    ) F ON NIDT.ISSUE_DATA_UID = F.ISSUE_DATA_UID
                    ORDER BY content DESC LIMIT 18446744073709551615
                    ) A GROUP BY content
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    result = pd.DataFrame(data,columns=['id', 'subject', 'description', 'issue_type', 'site_name', 'biz_title', 'issue_manage_user', 'created_on'])
    issue_list = []
    for row, value in result.iterrows():
        print("Issue id {} found. created on: {}".format(value['id'],value['created_on']))
        issue = ProductIssue(value['id'], value['subject'], value['description'], value['issue_type'],value['site_name'], value['biz_title'], value['issue_manage_user'], value['created_on'])
        issue_list.append(issue)

    cursor.close()
    cnx.close()
    return issue_list

# 엘라스틱서치에 출력하는 함수입니다. 
def issueToElasticSearch(issues):
    putUrlPrefix = 'http://localhost:9200/portal/_doc/'
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    for issue in issues:
        id = getUniqueIndexId(issue.title)
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

def begin_pingestor():
    p = getIssues()
    issueToElasticSearch(p)