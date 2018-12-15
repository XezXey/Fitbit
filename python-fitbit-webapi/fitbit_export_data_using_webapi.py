import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import sys

# More information about api can be found at https://dev.fitbit.com/build/reference/web-api/

# query_str to get heart rate in current date
query_str = 'https://api.fitbit.com/1/user/-/activities/heart/date/today/1d/1sec.json'

# secret token of application to access web-api
secret_token = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMkRGOFkiLCJzdWIiOiI3MkNOTjciLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJhY3QgcnNldCBybG9jIHJ3ZWkgcmhyIHJwcm8gcm51dCByc2xlIiwiZXhwIjoxNTQ1Mzg1MTAzLCJpYXQiOjE1NDQ3ODAzMDN9.hwlzNRGTCM75LXggSGreQvd8mM7bEf12OQZvStgM0Jo'

# filepath to write json file
path = './fitbit_hr.csv'
filename = 'fitbit_hr.csv'

# define authentication header to authenticate with fitbit server
secret_header = {'Authorization' : 'Bearer {}'.format(secret_token)}

# HTTP get to fitbit server with query string to get the data
response = requests.get(query_str, headers=secret_header)

# Writing data into json format file
with open(path, 'w') as f:
    json.dump(response.json(), f)

# Reading data into json format file
with open(path, 'r') as f:
    json_data = json.load(f)
    print(json_data)

# Create the dataframe of given data to contain the data and for export to csv fotmat file easily
df = pd.DataFrame(json_data['activities-heart-intraday']['dataset'])
plt.plot(df.head(100).time, df.head(100).value)
plt.show()

#start_experiment_time = datetime.datetime('').strftime("%Y-%m-%d_%H-%M-%S_")
start_experiment_time = sys.argv[1]
df.to_csv(start_experiment_time + filename)
