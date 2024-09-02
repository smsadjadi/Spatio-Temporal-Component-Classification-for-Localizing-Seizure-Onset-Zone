from scipy.ndimage import zoom
import numpy as np

def cluster_connectivity(fmri_data, mask):
    masked_voxels = fmri_data[mask > 0]
    time_series = masked_voxels.T
    connectivity_matrix = np.corrcoef(time_series.T)
    return connectivity_matrix

def cluster_connectivity_ds(fmri_data, mask, downsample_factor=2):
    if isinstance(downsample_factor, int):
        downsample_factor = (downsample_factor, downsample_factor, downsample_factor)
    downsampled_fmri = zoom(fmri_data, zoom=(1/downsample_factor[0], 1/downsample_factor[1], 1/downsample_factor[2], 1), order=1)
    downsampled_mask = zoom(mask, zoom=(1/downsample_factor[0], 1/downsample_factor[1], 1/downsample_factor[2]), order=0)
    masked_voxels = downsampled_fmri[downsampled_mask > 0]
    time_series = masked_voxels.T
    connectivity_matrix = np.corrcoef(time_series.T)    
    return connectivity_matrix

def voxel_network_strength(fmri_data, mask, voxel_index):
    if mask[voxel_index] == 0:
        raise ValueError("The specified voxel_index is not within the masked region.")
    time_series = fmri_data[mask > 0].T
    voxel_time_series = fmri_data[voxel_index].flatten()
    num_voxels = time_series.shape[1]
    network = np.zeros(num_voxels)
    for i in range(num_voxels):
        network[i] = np.corrcoef(time_series[:, i], voxel_time_series)[0, 1]
    network = np.sort(network)[::-1]
    network_strength = round(sum(network)/num_voxels,3)
    return network_strength

