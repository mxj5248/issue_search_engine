from db.es_util import delete_index
from db.es_pool import get_conn

def create_rsp_index():
    index = "idx_redminesp"
    delete_index(index)
    es = get_conn()
    payload = {
        "settings": {
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": 1
            },
            "analysis":{
                "analyzer":{
                    "korean_nori_analyzer":{
                        "type":"custom",
                        "tokenizer":"korean_nori_tokenizer",
                        "filter": [ "lowercase","my_shingle_f", "korean_posfilter" ]
                    },
                    "title_analyzer":{
                        "type":"custom",
                        "tokenizer":"whitespace",
                        "filter": [ "lowercase","my_shingle_f" ]

                    },
                },
                "tokenizer":{
                    "korean_nori_tokenizer":{
                        "type":"nori_tokenizer",
                        "decompound_mode":"mixed",
                        "discard_punctuation": "false",
                        "user_dictionary": "analysis/noun_list.txt"
                    }
                },
                "filter" : { 
                    "edge_ngram_filter_front": { "type": "edge_ngram", "min_gram": "2", "max_gram": "10", "side": "front" }, 
                    "edge_ngram_filter_back": { "type": "edge_ngram", "min_gram": "2", "max_gram": "10", "side": "back" },
                    "korean_posfilter":{ "type":"nori_part_of_speech", "stoptags":[ "E", "IC", "J", "MAG", "MM", "NA", "NR", "SC", "SE", "SF", "SP", "SSC", "SSO", "SY", "UNA", "VA", "VCN", "VCP", "XPN", "XR", "XSA", "XSN", "XSV" ] },
                    "my_shingle_f": {
                        "type": "shingle",
                        "min_shingle_size": 2,
                        "max_shingle_size": 3
                        }
                    },
            }
        },
        "mappings": {
            "properties": {
                "id": {
                    "type": "long"
                },
                "container_id":{
                    "type": "long"
                },
                "subject": {
                    "type": "text",
                    "analyzer": "title_analyzer"
                },
                "description": {
                    "type": "text",
                    "analyzer": "korean_nori_analyzer",
                },
                "created_on": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss||strict_date_optional_time ||epoch_millis"
                },
                "red_subject": {
                    "type": "text",
                    "analyzer": "title_analyzer"
                },
                "red_description": {
                    "type": "text",
                    "analyzer": "korean_nori_analyzer",
                },
            }
        }
    }

    headers = {
        'Content-Type': 'application/json'
    }

    es.indices.create(index=index, headers=headers, body=payload)

