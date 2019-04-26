import requests
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import sys
import errno

# More information about api can be found at https://dev.fitbit.com/build/reference/web-api/

# Reading a secret token of application to access web-api from current directory
# Access token need to store in "access_token.txt"
try: 
    with open('./access_token.txt', 'r') as access_token_file:
        secret_token = access_token_file.readlines()[0].strip('\n')
except FileNotFoundError :
    print('No access token file')
    exit()

# Get input date for specific date data acquisition : default = today
experiment_date = input("Input date(yyyy-MM-dd) that performed an experiment(default is today) : ")
if experiment_date == '':
    experiment_date = 'today'


# define authentication header to authenticate with fitbit server
secret_header = {'Authorization' : 'Bearer {}'.format(secret_token)}
# query_str_dict for each features to get data in current date
query_str_dict = {
    'heart' : 'https://api.fitbit.com/1/user/-/activities/heart/date/{0}/1d/1sec.json'.format(experiment_date), 
    'steps' : 'https://api.fitbit.com/1/user/-/activities/steps/date/{0}/1d.json'.format(experiment_date), 
    'minutesSedentary' : 'https://api.fitbit.com/1/user/-/activities/minutesSedentary/date/{0}/1d.json'.format(experiment_date), 
    'minutesLightlyActive' : 'https://api.fitbit.com/1/user/-/activities/minutesLightlyActive/date/{0}/1d.json'.format(experiment_date), 
    'minutesFairlyActive' : 'https://api.fitbit.com/1/user/-/activities/minutesFairlyActive/date/{0}/1d.json'.format(experiment_date), 
    'minutesVeryActive' : 'https://api.fitbit.com/1/user/-/activities/minutesVeryActive/date/{0}/1d.json'.format(experiment_date)
}
# feature_name_dict for renaming the columns name for each feature
feature_name_dict = {
    'heart' : 'HR_fitbit', 
    'steps' : 'Steps_fitbit',
    'minutesSedentary' : 'Sedentary_fitbit',
    'minutesLightlyActive' : 'LightlyActive_fitbit',
    'minutesFairlyActive' : 'FairlyActive_fitbit',
    'minutesVeryActive' : 'VeryActive_fitbit'
}

fitbit_df_dict = {} # store dataFrame of each feature
fitbit_json_dict = {} # store json data of each feature

# filepath to write json file
path = './dataset_fitbit/' + sys.argv[1] + '/'
filename_csv = 'fitbit_data.csv'
filename_json = 'fitbit_data.json'
start_experiment_time = sys.argv[1]

# Try to make directory if it's not exist
if not os.path.exists(os.path.dirname(path)):
    try:
        os.makedirs(os.path.dirname(path))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise


fitbit_df = pd.DataFrame()
initial_flag = 0 # Flag for merge a dataFrame (preventing the empty_df merging) ===> always assign 1st df to initial merged dataframe
# Iterate over each keys(feature) then apply : adding date + renaming + merging
for each_feature in query_str_dict.keys():
    print("Data Acquisition : Feature {0}".format(each_feature))
    fitbit_json_dict[each_feature] = requests.get(query_str_dict[each_feature], headers=secret_header).json() # send HTTPS request for using web-api and get json data
    date = fitbit_json_dict[each_feature]['activities-{0}'.format(each_feature)][0]['dateTime'] # get date by feature
    fitbit_df_dict[each_feature] = pd.DataFrame(fitbit_json_dict[each_feature]['activities-{0}-intraday'.format(each_feature)]['dataset']) # get data by feature
    fitbit_df_dict[each_feature].rename(columns={'time':'Timestamp', 'value':feature_name_dict[each_feature]}, inplace=True) # renaming
    fitbit_df_dict[each_feature]['Timestamp'] = fitbit_df_dict[each_feature]['Timestamp'].apply(lambda each_time : date + '_' + each_time) # adding date
    # merging
    if initial_flag == 0: # assign first df for prevent a empty dataframe
        fitbit_df = fitbit_df_dict[each_feature]
        initial_flag = 1
    else : 
        fitbit_df = pd.merge(fitbit_df, fitbit_df_dict[each_feature], on='Timestamp', how='outer', sort=True) # Merge by outer join(Union), on 'Timestamp' column and sort by 'Timestamp'

# Saving to csv file
fitbit_df.to_csv(path + start_experiment_time + filename_csv)
print(fitbit_df_dict)
print(fitbit_df)


