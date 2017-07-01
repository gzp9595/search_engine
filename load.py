import json
import formatter


file_name = "data/law/small_data/" + "54f84249-ee8c-4a7d-bec5-a7480126f94e_content.json"

f = open(file_name, "r")

content = ""

for line in f:
    content = json.loads(line)
    break

for x in content:
    print x, content[x]


formatter.parse(content)