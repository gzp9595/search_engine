import os

os.system("curl -XPUT http://localhost:9200/law")
print

print
os.system("""curl -XPOST http://localhost:9200/law/big_data/_mapping -d'
{
    "big_data": {
        "_all": {
            "analyzer": "ik_smart",
            "search_analyzer": "ik_smart",
            "term_vector": "no",
            "store": "false"
        },  
        "properties": {
            "content": {
                "type": "text",
                "analyzer": "ik_smart",
                "search_analyzer": "ik_smart",
                "include_in_all": "true",
                "boost": 8
            },
            "Title": {
                "type": "text",
                "analyzer": "ik_smart",
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
os.system("""curl -XPOST http://localhost:9200/law/content/_mapping -d'
{
    "content": {
        "properties": {
            "content": {
                "type": "text",
                "analyzer": "ik_smart",
                "search_analyzer": "ik_smart",
                "include_in_all": "true",
                "boost": 8
            },
            "Title": {
                "type": "text",
                "analyzer": "ik_smart",
                "search_analyzer": "ik_smart",
                "include_in_all": "true",
                "boost": 8
            }
        }
    }
}'""")
