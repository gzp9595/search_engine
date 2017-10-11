import os

os.system("curl -XPUT http://localhost:9200/law_meta")
print
os.system("""curl -XPOST http://localhost:9200/law_meta/meta/_mapping -d'
{
    "meta": {
        "_all": {
            "index" : "no"
        },
        "properties": {
            "FLYJ": {
                "type" : "nested",
                "index" : "no
            }
        }
    }
}'""")
