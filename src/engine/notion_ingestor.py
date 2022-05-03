import requests
import json
import pandas as pd

def create_nt_index():
    url = "https://api.notion.com/v1/databases/d22323a20ddc41d2b89a3d4990442309/query"
    payload = json.dumps({
    })
    headers = {
        'Authorization': 'Bearer secret_lrHfKHS6SaaMVkNVlISGpMxROOxeHHsoQH1z4mgZmmr',
        'Content-Type': 'application/json',
        'Notion-Version': '2021-05-13'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    # print(response.text)
    data = response.json()
    return data

data = create_nt_index()
# print(data['results'])
result = pd.DataFrame(data['results'])
# print(result)
# for s in :
    # print(s)
# for s in :
    # for st in s:
# 
    #    print(st)
        # print('-------------------------------')