import json
import requests

response = requests.get("https://jsonplaceholder.typicode.com/todos")
todos = json.loads(response.text)

user = 8

for dict in todos:
    if(dict["userId"] == user):
        print( "-"*100, "\n ", "\t\t [", " ❌ " if(dict["completed"] == False) else " ✅ ", "]" ,":", dict["title"])
