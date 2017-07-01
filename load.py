import json
import formatter


file_name = "data/law/small_data/" + "010cdb54-374f-47df-ba6e-a74a01869990_content.json"

f = open(file_name, "r")

content = ""

for line in f:
    content = json.loads(line)
    break

for x in content:
    print x, content[x]


formatter.parse(content)