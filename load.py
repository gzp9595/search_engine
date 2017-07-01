import json
import formatter


file_name = "data/law/small_data/" + "f6110808-45f9-4e7b-901a-a74a01869b15_content.json"

f = open(file_name, "r")

content = ""

for line in f:
    content = json.loads(line)
    break

for x in content:
    print x, content[x]


formatter.parse(content)