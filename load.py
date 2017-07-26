import json
import formatter

file_name = "data/law/small_data/" + "47c310f1-7bd9-44eb-a8c4-a748008c9e52_content.json"

f = open(file_name, "r")

content = ""

for line in f:
    content = json.loads(line)
    break
content = formatter.parse(content)

for x in content:
    print x, content[x]
