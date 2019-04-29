#!/bin/bash
# Reading file experiment_date_list.txt and iterate over each subject:experiment_date
# to pull the data using "fitbit_export_data_using_webapi.py" script
experiment_date_list_file="./experiment_date_list.txt"
while IFS= read -r experiment # Reading file from experiment_date_list_file into experiment line by line
do
    IFS=$' '  read subject experiment_date <<< $experiment # read and split to subject, experiment_date using ' '(space)
    #echo "$subject"
    #echo "$experiment_date"
    echo "$experiment_date" | python ./fitbit_export_data_using_webapi.py $subject # Running python script
    sleep 5 # Sleep for 2.5 seconds to prevents request limit exceed
done < "$experiment_date_list_file"
