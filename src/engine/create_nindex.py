import requests
import json
from db.es_util import delete_index
from db.es_pool import get_conn

def create_nt_index():
    # url = "http://localhost:9200/notion"
    index = "notion"
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
                    "edge_ngram_filter_front": { "type": "edgeNGram", "min_gram": "2", "max_gram": "10", "side": "front" }, 
                    "edge_ngram_filter_back": { "type": "edgeNGram", "min_gram": "2", "max_gram": "10", "side": "back" },
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
                "subject": { #제목
                        "type": "text"
                    },
                "description": { #업무내용 
                        "type": "text"
                    },
                "content_type": { # 유형
                    "type":"text"
                },
                "write_user": { # 작성자
                    "type":"text"
                },
                "hash_tag": { # 해시태그
                    "type":"text"
                },
                "created_on": { # 생성시점 
                        "type": "date"
                },
            }
        }
    }
    headers = {
        'Content-Type': 'application/json'
    }

    es.indices.create(index=index, headers=headers, body=payload)