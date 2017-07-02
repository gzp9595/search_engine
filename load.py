import json
import formatter


file_name = "data/law/small_data/" + "c80a5f66-0000-4f89-887e-a74b00b957b7_content.json"

f = open(file_name, "r")

content = ""

for line in f:
    content = json.loads(line)
    break
content = formatter.parse(content)

for x in content:
    print x, content[x]


