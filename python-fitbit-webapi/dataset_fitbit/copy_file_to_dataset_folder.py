import os
import shutil
import glob
src_path = "/home/puntawat/SleepTeam/SleepExperiment_Data_Acquisition/Fitbit/Python_Fitbit/python-fitbit-webapi/dataset_fitbit/"
dest_path = "/home/puntawat/SleepTeam/SleepExperiment_Dataset/SleepExperimentDataset_Debugging/"

print(os.listdir(src_path))
print(os.listdir(dest_path))

n_subject = 21
for subject_idx in range(1, n_subject+1):
    src_files = os.listdir(src_path + 'subject{:02d}/'.format(subject_idx))
    print(src_files)
    for file_name in src_files:
        full_file_name = os.path.join(src_path + 'subject{:02d}/'.format(subject_idx) + file_name)
        print(full_file_name)
        if (os.path.isfile(full_file_name)):
            shutil.copy(full_file_name, glob.glob(dest_path + 'Subject{:02d}*'.format(subject_idx))[0] + '/Fitbit/')