import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
query_str = 'https://api.fitbit.com/1/user/-/activities/heart/date/today/1d/1sec.json'
secret_token = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMkRGOFkiLCJzdWIiOiI3MkNOTjciLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJhY3QgcnNldCBybG9jIHJ3ZWkgcmhyIHJwcm8gcm51dCByc2xlIiwiZXhwIjoxNTQ1Mzg1MTAzLCJpYXQiOjE1NDQ3ODAzMDN9.hwlzNRGTCM75LXggSGreQvd8mM7bEf12OQZvStgM0Jo'
path = './fitbit_hr.csv'

secret_header = {'Authorization' : 'Bearer {}'.format(secret_token)}

response = requests.get(query_str, headers=secret_header)
with open(path, 'w') as f:
    json.dump(response.json(), f)

with open(path, 'r') as f:
    json_data = json.load(f)
    print(json_data)

df = pd.DataFrame(json_data['activities-heart-intraday']['dataset'])
print(df.head(5))
plt.plot(df.head(100).time, df.head(100).value)
plt.show()
df.to_csv(path)
