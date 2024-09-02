import numpy as np
import scipy as sp

def morphological_operation(input_array, disk_radius=2):
    
    structure = sp.ndimage.generate_binary_structure(input_array.ndim, 1)
    structure = sp.ndimage.binary_dilation(structure, iterations=disk_radius)
    array = sp.ndimage.binary_opening(input_array, structure=structure)
    structure = sp.ndimage.binary_dilation(structure, iterations=disk_radius)
    output_array = sp.ndimage.binary_closing(array, structure=structure)
    output_array = output_array.astype(int)
    if np.sum(output_array) == 0: output_array = input_array
    
    return output_array