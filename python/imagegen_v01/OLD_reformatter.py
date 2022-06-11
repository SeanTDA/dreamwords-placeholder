
import json



with open('structures.json', 'r') as f:
    structureData = json.load(f)


newData = []

for structure in structureData:
    newData.append({"data":structure,"weight":1})
    

print(newData)
with open('data.json', 'w') as f:
    json.dump(newData, f)
