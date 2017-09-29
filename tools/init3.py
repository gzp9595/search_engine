import os

os.system("curl -XPUT http://localhost:9200/law_doc")
print

print
os.system("""curl -XPOST http://localhost:9200/law_doc/content_seg/_mapping -d'
{
    "content_seg": {
        "properties": {
            "content": {
                "type": "text",
                "analyzer": "no_thulac",
                "search_analyzer": "thulac",
                "include_in_all": "true",
                "boost": 8
            }
        }
    }
}'""")

