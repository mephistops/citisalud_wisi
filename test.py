import json
import requests
from requests.auth import HTTPBasicAuth

psa_url = 'http://186.1.162.202:8081/api/pte_oodo'
psa_username = '1045693633'
psa_password = '12345'
psa_hash_key = '8606da74dd0724699bc874bc9348c678'
psa_date_ini = '2021-08-01'
psa_date_end = '2021-08-01'

url = psa_url
hash_key = psa_hash_key
username = psa_username
password = psa_password

datos = {
    "hash_key": hash_key,
    "json": {
        "fecha_ini": psa_date_ini,
        "fecha_fin": psa_date_end
    }
}

response = requests.post(url,
                         auth=(username, password),
                         headers={'Content-Type': 'application/json'},
                         json=datos)

print(json.loads(response.text))
