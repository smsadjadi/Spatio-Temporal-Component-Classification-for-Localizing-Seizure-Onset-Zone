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
        if subject_id < 10: file_path = f'{directory_path}/Sub0{subject_id}_sIC_Features.csv'
        else: file_path = f'{directory_path}/Sub{subject_id}_sIC_Features.csv'
        df = pd.read_csv(file_path)
        if subject_id == 1: header=True
        else: header=False
        df.to_csv(os.path.join(directory_path,output_file), mode='a', index=False, header=header)

def rename_column_in_csv(folder_path, old_column_name, new_column_name):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            if old_column_name in df.columns:  
                df.rename(columns={old_column_name: new_column_name}, inplace=True)
                df.to_csv(file_path, index=False)
                print(f"Processed and renamed column in file: {file_name}")
            else:
                print(f"Column '{old_column_name}' not found in {file_name}")

def remove_column_from_csv(folder_path, column_name):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            if column_name in df.columns:  
                df = df.drop(column_name, axis=1)
                df.to_csv(file_path, index=False)
                print(f"Removed column from file: {file_name}")
            else:
                print(f"Column '{column_name}' not found in {file_name}")