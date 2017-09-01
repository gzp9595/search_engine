import os

os.system("curl -XPUT http://localhost:9200/law_thulac")
print

print
os.system("""curl -XPOST http://localhost:9200/law_thulac/big_data/_mapping -d'
{
    "big_data": {
        "_all": {
            "type": "text",
            "analyzer": "thulac",
            "search_analyzer": "thulac",
            "include_in_all": "true",
            "boost": 8
        }
    }
}'""")


print
os.system("""curl -XPOST http://localhost:9200/law/law_thulac/_mapping -d'
{
    "content": {
        "properties": {
            "content": {
                "type": "text",
                "analyzer": "thulac",
                "search_analyzer": "thulac",
                "include_in_all": "true",
                "boost": 8
            },
            "Title": {
                "type": "text",
                "analyzer": "thulac",
                "search_analyzer": "thulac",
                "include_in_all": "true",
                "boost": 8
            }
        }
    }
}'""")
