import numpy as np

def mean_fmri_in_neighborhood(fmri_data, coord_index, radius):
    
    x_max, y_max, z_max, _ = fmri_data.shape
    radius = int(radius)
    x, y, z = coord_index

    x_min = max(x - radius, 0)
    x_max = min(x + radius + 1, fmri_data.shape[0])
    y_min = max(y - radius, 0)
    y_max = min(y + radius + 1, fmri_data.shape[1])
    z_min = max(z - radius, 0)
    z_max = min(z + radius + 1, fmri_data.shape[2])

    neighborhood_data = fmri_data[x_min:x_max, y_min:y_max, z_min:z_max, :]
    mean_signal = np.mean(neighborhood_data, axis=(0, 1, 2))

    return mean_signal

