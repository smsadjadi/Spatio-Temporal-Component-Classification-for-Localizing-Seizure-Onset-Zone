import numpy as np
import nilearn as nil
from nilearn import image

def ic_browse(selected_ic, criterion, affine, show=True):
    
    # Criterion Examples:
    # # selected_ic >= selected_ic.max()
    # # selected_ic >= selected_ic.flatten()[np.argsort(selected_ic.flatten())[-10:]][0]
    # # selected_ic >= 3.1
    
    places = np.where(criterion)
    indices = list(zip(places[0], places[1], places[2]))
    ijk_coords = []
    mni_coords = []

    for idx in indices:
        ijk_coords.append((selected_ic.shape[0]-idx[0],idx[1]+1,idx[2]+1))
        mni_coords.append(image.coord_transform(idx[0], idx[1], idx[2], affine))
    
    coords = {"Max_index": indices, "ijk_coords": ijk_coords, "MNI_coords": mni_coords}
    
    if show:
        print('')    
        print ('criterion indices:',coords["Max_index"])
        print ('XYZ coordinates:  ',coords["ijk_coords"])
        print ('MNI coordinates:  ',coords["MNI_coords"])
    
    output_mask = np.zeros_like(selected_ic)
    output_mask[places] = 1
    
    return coords, output_mask