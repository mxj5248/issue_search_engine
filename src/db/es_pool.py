from elasticsearch import Elasticsearch

def get_conn():
    es = Elasticsearch("http://elasticsearch:9200")
    return es