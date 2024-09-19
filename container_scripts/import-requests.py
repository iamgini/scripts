import requests

url = "https://api.openshift.com/api/serviceregistry_mgmt/v1/registries"

headers = {"Content-Type": "application/json"}

response = requests.get(url, headers=headers)

print(response.json())