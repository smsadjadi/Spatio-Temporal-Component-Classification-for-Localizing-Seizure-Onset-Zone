import scipy as sp

def morphological_operation(array, disk_radius=2):
    
    structure = sp.ndimage.generate_binary_structure(array.ndim, 1)
    structure = sp.ndimage.binary_dilation(structure, iterations=disk_radius)
    array = sp.ndimage.binary_opening(array, structure=structure)
    structure = sp.ndimage.binary_dilation(structure, iterations=disk_radius)
    array = sp.ndimage.binary_closing(array, structure=structure)
    array = array.astype(int)
    
    return array