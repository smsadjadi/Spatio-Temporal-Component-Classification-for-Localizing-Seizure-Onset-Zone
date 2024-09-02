import scipy as sp
import numpy as np

def mask_cc_around_coordinate(array, coordinate):
    
    structure = sp.ndimage.generate_binary_structure(array.ndim, 1)
    labeled_array,_ = sp.ndimage.label(array, structure=structure)
    component_label = labeled_array[coordinate]
    
    component_indices = np.where(labeled_array == component_label)
    
    mask = np.zeros_like(array)
    mask[component_indices] = 1

    return mask