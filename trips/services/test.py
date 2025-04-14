import json

with open('/home/dima/Documents/cities.json', 'r') as cities:
    a = json.load(cities)
print(a[0])
