import requests
import json

url = "http://localhost:9200/issues"

payload = json.dumps({
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
                    # "filter": [ "lowercase", "my_shingle_f","korean_posfilter", "edge_ngram_filter_front","edge_ngram_filter_back","trim" ]
                    "filter": [ "lowercase","my_shingle_f" ]

                },
                "title_analyzer":{
                    "type":"custom",
                    "tokenizer":"whitespace",
                    # "filter": [ "lowercase", "my_shingle_f", "korean_posfilter", "edge_ngram_filter_front","edge_ngram_filter_back", "trim" ]
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
                # "synonym_filter": { "type": "synonym", "lenient": "true", "synonyms_path":"analysis/synonyms.txt" },
                "korean_posfilter":{ "type":"nori_part_of_speech", "stoptags":[ "E", "IC", "J", "MAG", "MM", "NA", "NR", "SC", "SE", "SF", "SP", "SSC", "SSO", "SY", "UNA", "VA", "VCN", "VCP", "XPN", "XR", "XSA", "XSN", "XSV" ] },
                "my_shingle_f": {
                    "type": "shingle",
                    "min_shingle_size": 2,
                    "max_shingle_size": 3
                    }
                # "synonym" : { 
                #     "type" : "synonym", 
                #     "ignore_case": "true",
                #     "synonyms_path" : "analysis/synonyms.txt",
                #     }
                },
        }
        # "analysis": {
        #     "filter" : { 
        #         "synonym" : { 
        #             "type" : "synonym", 
        #             "ignore_case": "true",
        #             "synonyms_path" : "analysis/synonyms.txt",
        #             }
        #         },
        #     "analyzer": {
        #         "synonym": {
        #             "type": "custom",
        #             "tokenizer": "my_ngram",
        #             "filter": ["lowercase","synonym"]
        #             },
        #         "keyword_analyzer": {
        #             "filter": ["lowercase"],
        #             "char_filter": [],
        #             "type": "custom",
        #             "tokenizer": "keyword"
        #         },
        #         "edge_ngram_analyzer": {
        #             "filter": ["lowercase"],
        #             "tokenizer": "lowercase"
        #         },
        #         "edge_ngram_search_analyzer": {
        #             # "tokenizer": "edge_ngram_tokenizer"
        #             # "tokenizer": "keyword"
        #             "tokenizer": "nori_mixed",
        #             }
        #         },
        # "tokenizer": {
        #         # "my_ngram": {
        #         #     "type": "ngram",
        #         #     "min_gram": 2,
        #         #     "max_gram": 3,
        #         #     "token_chars": [
        #         #     "letter",
        #         #     "digit"
        #         #     ]
        #         # }
        #         "nori_mixed": {
        #             "type": "nori_tokenizer",
        #             "decompound_mode": "mixed"
        #             }
        #     }
        # }
    },
    "mappings": {
        "properties": {
            "id": {
                "type": "long"
            },
            "subject": {
                "type": "text",
                "analyzer": "title_analyzer"
            },
            "description": {
                "type": "text",
                # "analyzer": "korean_nori_analyzer",
                # "search_analyzer": "title_analyzer"            
            },
            "tracker_id": {
                "type": "long"
            },
            "project_id": {
                "type": "long"
            },
            "status_id": {
                "type": "long"
            },
            "created_on": {
                "type": "date",
            },
            "updated_on": {
                "type": "date",
                # "format": "yyyy-MM-dd HH:mm:ss"
            }
        }
    }
})
headers = {
    'Content-Type': 'application/json'
}

response = requests.request("PUT", url, headers=headers, data=payload)

print(response.text)
