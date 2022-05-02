import requests
import json
import pandas as pd
import dash 
import dash_core_components as dcc
import dash_html_components as html
from elasticsearch import Elasticsearch
import pprint

# def generate_table(dataframe, max_rows=26):
#     return html.Table(
#         # Header
#         [html.Tr([html.Th(col) for col in dataframe.columns]) ] +
#         # Body
#         [html.Tr([
#             html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
#         ]) for i in range(min(len(dataframe), max_rows))]
#     )
# url = 'http://localhost'
# port = '9200'
# global es 
# # es = Elasticsearch(f'{url}:{port}')
# es = Elasticsearch(hosts=[{"host": 'http://localhost', "port": 9200}], connection_class=RequestsHttpConnection, max_retries=30,
#                        retry_on_timeout=True, request_timeout=30)


def search(keyword=None):
    body =  {
        "query": {
            "multi_match": {
                "type": "best_fields",
                "fields": [
                    "subject", 
                "description"
            ],
                "query": keyword,
            }
        },
    # }
        "highlight": {
            "fragment_size": 150,
            "fields": {
                "subject": {},
                "description": {}
            }
        },
    }

    es = Elasticsearch("http://localhost:9200")
    res = es.search(index='issues',body=body)
    return res
    
r = search("mha 동기화")
# pprint.pprint(r)
row = r['hits']['hits']
print(row[0]['highlight'])
# input_value = 'mha 동기화'
# input_address = 'http://localhost:9200/issues/_search?q=' + input_value
# res = requests.get(input_address)
# json_data = res.json()
# print(json_data)
# # row = json_data['hits']['hits']
# row = json_data['hits']
# print(row)

# input_address = 'http://localhost:9200/issues/_search'
# from elasticsearch import Elasticsearch
# elastic_client = Elasticsearch(hosts=["http://localhost:9200"])

# # User makes a request on client side
# # user_request = "some_param"

# # Take the user's parameters and put them into a Python
# # dictionary structured like an Elasticsearch query:
# # query_body = {
# #   "query": {
# #     "bool": {
# #       "must": {
# #         "match": {      
# #           "some_field": user_request
# #         }
# #       }
# #     }
# #   }
# # }
# query_body = {
#   "query": {
#     "multi_match": {
#       "query": "database",
#       "fields": ["subject", "description"]
#     }
#   },
# }
# # call the client's search() method, and have it return results
# results = elastic_client.search(index="issues", body=query_body)
# print(results)
# for result in results['hits']['hits']:
#     print('score:', result['_score'], 'source:', result['_source'])


# print(res)
# json_data = res.json()
# print(json_data)
# row = json_data['hits']['hits']
# row = json_data['hits']
# print(row)
# data = {}


# for r in row: 
#     data["이슈번호"]= [str(r['_source']['id'])]
#     data["제목"]=[r['_source']['subject']]
#     data["매치율"] = [str(r['_score'])]
#     data['상세설명'] = [r['_source']['description']]
#     # results.append(html.P("이슈번호 : "+ str(r['_source']['id']) +' '+ r['_source']['subject'] + ' (score: ' + str(r['_score'])+ ')'))
#     # results.append(html.P("상세설명 : " + r['_source']['description'] ))
#     # results.append(html.Br())
# print(data)
# df = pd.DataFrame(data)
# # print(row['_source']['subject'])
# print(df)