import nibabel as nib
import nilearn as nil
import numpy as np

from EDA import *
from dataloaders import *
from utils import *
import config

dataset_dir = config.dataset_dir
ez_ics = [(1,16),(2,17),(3,13),(4,15),(5,27),(6,17),(7,26),(8,4),(9,15),(10,10)]

for ic in ez_ics:
    
    subject_id = ic[0]
    ez_ic = ic[1]
    
    bold, _ = data_import(dataset    = dataset_dir,
                          subject_id = subject_id,
                          subfolder  = 'pre_bold\\pre_bold_preprocessed.ica',
                          data_name  = ['filtered_func_data'])

    fmri_data = bold['filtered_func_data'].get_fdata()

    sica, save_dir = data_import(dataset    = dataset_dir,
                                 subject_id = subject_id,
                                 subfolder  = 'pre_bold\\pre_bold_preprocessed.ica\\filtered_func_data.ica',
                                 data_name  = ['mask','melodic_IC'])

    selected_ic = ic_extract(sica['melodic_IC'],ez_ic)

    _, selected_ic_cluster = ic_browse(selected_ic = selected_ic,
                                       criterion   = selected_ic >= 3.1,
                                       affine      = sica['melodic_IC'].affine,
                                       show        = False)

    selected_ic_cluster = morphological_operation(selected_ic_cluster)

    max_value, _ = ic_browse(selected_ic = selected_ic,
                             criterion   = selected_ic >= selected_ic.max(),
                             affine      = sica['melodic_IC'].affine,
                             show        = False)

    selected_ic_mask = mask_cc_around_coordinate(selected_ic_cluster, max_value["Max_index"][0])
    selected_ic_masked = selected_ic_mask * selected_ic
    selected_ic_fMRI = np.expand_dims(selected_ic_mask, axis=-1) * fmri_data

    nifti_save(array  = selected_ic_cluster,
            affine = sica['melodic_IC'].affine,
            dir    = save_dir,
            name   = 'ez_cluster')

    nifti_save(array  = selected_ic_masked,
            affine = sica['melodic_IC'].affine,
            dir    = save_dir,
            name   = 'ez_area')

    nifti_save(array  = selected_ic_fMRI,
            affine = sica['melodic_IC'].affine,
            dir    = save_dir,
            name   = 'ez_fmri')

    print('')