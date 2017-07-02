import json
import formatter


file_name = "data/law/small_data/" + "48e3c0f1-3c8c-4d6a-8b1f-a7480126e14d_content.json"

f = open(file_name, "r")

content = ""

for line in f:
    content = json.loads(line)
    break

for x in content:
    print x, content[x]


formatter.parse(content)