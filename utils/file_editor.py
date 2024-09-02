import pandas as pd
import numpy as np
import os

def remove_suffix_from_folders(root, name, suffix):
    if name.endswith(suffix):
        new_name = name[:-len(suffix)]
        old_path = os.path.join(root, name)
        new_path = os.path.join(root, new_name)
        os.rename(old_path, new_path)
        print(f"Renamed: {old_path} to {new_path}")

def rename_folders(directory, suffix):
    for root, dirs, files in os.walk(directory, topdown=False):
        for file_name in files:
            remove_suffix_from_folders(root, file_name, suffix)
        for dir_name in dirs:
            remove_suffix_from_folders(root, dir_name, suffix)

def replace_suffix_in_files(root, name, old_suffix, new_suffix):
    if name.endswith(old_suffix):
        new_name = name.replace(old_suffix, new_suffix)
    else:
        return
    old_path = os.path.join(root, name)
    new_path = os.path.join(root, new_name)
    os.rename(old_path, new_path)
    print(f"Renamed: {old_path} to {new_path}")

def rename_files(directory, old_suffix, new_suffix):
    for root, _, files in os.walk(directory):
        for file_name in files:
            replace_suffix_in_files(root, file_name, old_suffix, new_suffix)

def merge_csv_files(directory_path, output_file):
    for subject_id in range(10):
        subject_id +=1
        file_path = os.path.join(directory_path,f"Sub{subject_id}_sIC_Features.csv")
        df = pd.read_csv(file_path)
        if subject_id == 1: header=True
        else: header=False
        df.to_csv(os.path.join(directory_path,output_file), mode='a', index=False, header=header)