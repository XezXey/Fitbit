import requests
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import sys

# More information about api can be found at https://dev.fitbit.com/build/reference/web-api/

# query_str to get heart rate in current date
query_str = 'https://api.fitbit.com/1/user/-/activities/heart/date/today/1d/1sec.json'

# secret token of application to access web-api
secret_token = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMkRGOFkiLCJzdWIiOiI3MkNOTjciLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcmFjdCBybG9jIHJ3ZWkgcmhyIHJwcm8gcm51dCByc2xlIiwiZXhwIjoxNTQ3NzIwMTM5LCJpYXQiOjE1NDcxMTU1Mjl9.WFJJitHH4IsKvvfzd8auPOSwJIAegWlw7rpGrT4wl5Q'


# filepath to write json file
path = './dataset_fitbit/' + sys.argv[1] + '/'
filename_csv = 'fitbit_hr.csv'
filename_json = 'fitbit_hr.json'
start_experiment_time = sys.argv[1]

# define authentication header to authenticate with fitbit server
secret_header = {'Authorization' : 'Bearer {}'.format(secret_token)}

# HTTP get to fitbit server with query string to get the data
response = requests.get(query_str, headers=secret_header)

# Try to make directory if it's not exist
if not os.path.exists(os.path.dirname(path)):
    try:
        os.makedirs(os.path.dirname(path))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

# Writing data into json format file
with open(path + start_experiment_time + filename_json, 'w') as f:
    json.dump(response.json(), f)

# Reading data into json format file
with open(path + start_experiment_time + filename_json, 'r') as f:
    json_data = json.load(f)
    #print(json_data)

# Create the dataframe of given data to contain the data and for export to csv fotmat file easily
df = pd.DataFrame(json_data['activities-heart-intraday']['dataset'])
#plt.plot(df.time, df.value)
#plt.show()

df.to_csv(path + start_experiment_time + filename_csv)
