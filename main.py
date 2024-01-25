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

_ , selected_ic_cluster = ic_browse(selected_ic = selected_ic,
                                    criterion   = selected_ic >= 2.9,
                                    affine      = sica['melodic_IC'].affine,
                                    show        = False)

indices, _ = ic_browse(selected_ic = selected_ic,
                       criterion   = selected_ic >= selected_ic.max(),
                       affine      = sica['melodic_IC'].affine,
                       show        = True)

selected_ic_cluster = morphological_operation(selected_ic_cluster)

selected_ic_mask = mask_cc_around_coordinate(selected_ic_cluster, indices[0])

selected_ic_masked = selected_ic_mask * selected_ic

nifti_save(array  = selected_ic_cluster,
           affine = sica['melodic_IC'].affine,
           dir    = save_dir,
           name   = 'ez_cluster')

nifti_save(array  = selected_ic_masked,
           affine = sica['melodic_IC'].affine,
           dir    = save_dir,
           name   = 'ez_area')