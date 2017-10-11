import os

os.system("curl -XPUT http://localhost:9200/law_vector")
print

print
os.system("""curl -XPOST http://localhost:9200/law_vector/tfidf/_mapping -d'
{
    "tfidf": {
        "_all": {
            "type": "text",
            "index" : "no"
        }
    }
}'""")
print
os.system("""curl -XPOST http://localhost:9200/law_vector/lda/_mapping -d'
{
    "lda": {
        "_all": {
            "type": "text",
            "index" : "no"
        }
    }
}'""")
print
os.system("""curl -XPOST http://localhost:9200/law_vector/word/_mapping -d'
{
    "word": {
        "_all": {
            "type": "text",
            "index" : "no"
        }
    }
}'""")
