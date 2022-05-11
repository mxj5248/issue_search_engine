import requests

url = "http://localhost:9200/idx_notion"

payload = ""
headers = {}

response = requests.request("DELETE", url, headers=headers, data=payload)

print(response.text)