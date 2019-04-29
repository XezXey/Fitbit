#!/bin/bash
# Reading file experiment_date_list.txt and iterate over each subject:experiment_date
# to pull the data using "fitbit_export_data_using_webapi.py" script
experiment_date_list_file="./experiment_date_list.txt"
while IFS= read -r experiment
do
    IFS=$' '  read subject experiment_date <<< $experiment
    #echo "$subject"
    #echo "$experiment_date"
    echo "$experiment_date" | python ./fitbit_export_data_using_webapi.py $subject
done < "$experiment_date_list_file"
