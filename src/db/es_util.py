# check es index
# import requests

# url = "http://localhost:9200/issues/_search"

# payload = {}
# headers = {}

# response = requests.request("GET", url, headers=headers, data=payload)

# print(response.text)


#delete
# import requests

# url = "http://localhost:9200/issues"

# payload = ""
# headers = {}

# response = requests.request("DELETE", url, headers=headers, data=payload)

# print(response.text)


# #get ex schema
# import requests

# url = "http://localhost:9200/issues"

# payload = ""
# headers = {}

# response = requests.request("GET", url, headers=headers, data=payload)

# print(response.text)

from db.es_pool import get_conn

global es
es = get_conn()

# def create_index(index,body=None):
#     if not es.indices.exists(index=index):
#         if body is None:
#             r = es.indices.create(index=index)
#         else: 
#             r = es.indices.create(index=index, body=body)
#         return r

def delete_index(index):
    if es.indices.exists(index=index):
        return es.indices.delete(index=index)

def insert(index, body):
    return es.index(index=index, body=body)
