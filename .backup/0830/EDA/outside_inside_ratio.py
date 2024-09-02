import numpy as np
import nibabel as nib

def outside_inside_ratio(ic_map, brain_mask):
    
    if isinstance(ic_map, nib.Nifti1Image): ic_map = ic_map.get_fdata()
    if isinstance(brain_mask, nib.Nifti1Image): brain_mask = brain_mask.get_fdata()
    
    assert ic_map.shape == brain_mask.shape, "IC map and brain mask must have the same shape."
    
    whole_voxels = np.sum(ic_map != 0)
    voxels_inside = np.sum((ic_map != 0) & (brain_mask > 0))
    voxels_outside = whole_voxels - voxels_inside
    if voxels_inside == 0: raise ValueError("No non-zero voxels inside the brain mask. Cannot calculate ratio.")
    ratio_outside_inside = round(voxels_outside/voxels_inside, 3)
    
    return ratio_outside_inside