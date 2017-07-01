import json
import formatter


file_name = "data/law/small_data/" + "5e8f74b4-d45a-4e9f-ab1b-a7480126a763_content.json"

f = open(file_name, "r")

content = ""

for line in f:
    content = json.loads(line)
    break

for x in content:
    print x, content[x]


formatter.parse(content)