import os


os.system("curl -XPUT http://localhost:9200/law")
print
os.system("""curl -XPOST http://localhost:9200/law/small_data/_mapping -d'
{
    "small_data": {
        "_all": {
            "analyzer": "ik_max_word",
            "search_analyzer": "ik_smart",
            "term_vector": "no",
            "store": "false"
        },  
        "properties": {
            "content": {
                "type": "text",
                "analyzer": "ik_max_word",
                "search_analyzer": "ik_smart",
                "include_in_all": "true",
                "boost": 8
            },
            "Title": {
                "type": "text",
                "analyzer": "ik_max_word",
                "search_analyzer": "ik_smart",
                "include_in_all": "true",
                "boost": 8
            },
            "FLYJ": {
                "type" : "nested"
            }
        }
    }
}'""")
print

print
os.system("""curl -XPOST http://localhost:9200/law/big_data/_mapping -d'
{
    "big_data": {
        "_all": {
            "analyzer": "ik_max_word",
            "search_analyzer": "ik_smart",
            "term_vector": "no",
            "store": "false"
        },  
        "properties": {
            "content": {
                "type": "text",
                "analyzer": "ik_max_word",
                "search_analyzer": "ik_smart",
                "include_in_all": "true",
                "boost": 8
            },
            "Title": {
                "type": "text",
                "analyzer": "ik_max_word",
                "search_analyzer": "ik_smart",
                "include_in_all": "true",
                "boost": 8
            },
            "FLYJ": {
                "type" : "nested"
            }
        }
    }
}'""")

