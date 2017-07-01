import json
import formatter


file_name = "data/law/small_data/" + "1f50bd7a-e976-4263-9938-a7480126b876_content.json"

f = open(file_name, "r")

content = ""

for line in f:
    content = json.loads(line)
    break

for x in content:
    print x, content[x]


formatter.parse(content)