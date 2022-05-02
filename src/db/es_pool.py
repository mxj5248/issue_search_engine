from elasticsearch import Elasticsearch

url = "http://elasticsearch"
port = "9200"

def get_conn():
    es = Elasticsearch(f'{url}:{port}')
    return es