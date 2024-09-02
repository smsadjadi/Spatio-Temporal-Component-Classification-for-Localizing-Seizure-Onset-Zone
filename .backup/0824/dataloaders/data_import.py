import os
import glob
import nibabel as nib


def data_import(dataset,subject_id,subfolder,data_name):
    
    subjects_list = glob.glob(os.path.join(dataset,'Sub*'))
    dataset_dir = os.path.abspath(subjects_list[subject_id-1])
    nifti_files = [file for file in os.listdir(os.path.join(dataset_dir,subfolder)) if file.endswith('.nii.gz')]
    data_paths = [os.path.join(dataset_dir,subfolder,file) for file in nifti_files]
    
    selected_paths = []
    data = {col: [] for col in data_name}
    
    print('')
    print("selected data:")
    for name in data_name:
        try:
            address = data_paths[nifti_files.index(name+'.nii.gz')]
            selected_paths.append(address)
            data[name] = nib.load(address)
            print(address,' >> Shape:',data[name].shape)
        except:
            print(name+'.nii.gz not found!')
            
    if selected_paths==[] or len(data_name) != len(selected_paths):
        print("\nexisting data paths:")
        for path in data_paths: print(path)
    
    folder_dir = os.path.split(address)[:-1][0]
    
    return data, folder_dir