import os

os.system("curl -XPUT http://localhost:9200/law_thulac")
print
os.system("""curl -XPOST http://localhost:9200/law_thulac/big_data/_mapping -d'
{
    "big_data": {
        "_all": {
            "type": "text",
            "analyzer": "no_thulac",
            "search_analyzer": "thulac",
            "include_in_all": "true",
            "boost": 8
        },
        "properties": {
            "FLYJ": {
                "type" : "nested"
            }
        }
    }
}'""")
print
