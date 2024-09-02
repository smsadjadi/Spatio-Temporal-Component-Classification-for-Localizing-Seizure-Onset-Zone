import nibabel as nib
import nilearn as nil
import numpy as np

from EDA import *
from dataloaders import *
from utils import *
import config

bold, _ = data_import(dataset    = config.dataset_dir,
                      subject_id = config.subject_id,
                      subfolder  = 'Analysis.ica',
                      data_name  = ['filtered_func_data'])

sica, save_dir = data_import(dataset    = config.dataset_dir,
                             subject_id = config.subject_id,
                             subfolder  = 'Analysis.ica\\filtered_func_data.ica',
                             data_name  = ['mask','melodic_IC'])

selected_ic = ic_extract(sica['melodic_IC'],config.sic_candidate)

indices, selected_ic_cluster = ic_browse(selected_ic = selected_ic,
                                         criterion   = selected_ic >= 3.1,
                                         affine      = sica['melodic_IC'].affine,
                                         show        = False)

max_value, _ = ic_browse(selected_ic = selected_ic,
                         criterion   = selected_ic >= selected_ic.max(),
                         affine      = sica['melodic_IC'].affine,
                         show        = True)

selected_ic_cluster = morphological_operation(selected_ic_cluster)

selected_ic_mask = mask_cc_around_coordinate(selected_ic_cluster, max_value[0])

selected_ic_masked = selected_ic_mask * selected_ic

selected_ic_fMRI = np.expand_dims(selected_ic_mask, axis=-1) * bold['filtered_func_data'].get_fdata()

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