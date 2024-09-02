import numpy as np

def binary_lateralization(IC_matrix, mask=None):
    # Ensure the input is of the correct shape
    if IC_matrix.shape != (91, 109, 91):
        raise ValueError("IC_matrix must be of shape (91, 109, 91)")
    
    if mask is not None and mask.shape != IC_matrix.shape:
        raise ValueError("Mask must be of the same shape as IC_matrix")

    # Define the ACPC plane (mid-sagittal plane)
    mid_plane_index = 45  # This is the zero-based index for the mid-sagittal plane
    
    left_binary_lateralized = 0
    right_binary_lateralized = 0
    total_binary_voxels = 0
    
    # Extract mirroring voxels from both sides of the brain
    for x in range(mid_plane_index):
        mirrored_x = IC_matrix.shape[0] - 1 - x  # Find the mirroring voxel
        right_voxels_slice = IC_matrix[x, :, :]
        left_voxels_slice = IC_matrix[mirrored_x, :, :]

        if mask is not None:
            # Apply mask
            left_voxels_slice = right_voxels_slice[mask[x, :, :] > 0]
            right_voxels_slice = left_voxels_slice[mask[mirrored_x, :, :] > 0]

        # Binary lateralization check
        left_voxels_binary = (left_voxels_slice > 0).astype(int)
        right_voxels_binary = (right_voxels_slice > 0).astype(int)
        
        # Update binary lateralization count
        left_binary_lateralized += np.sum(left_voxels_binary > right_voxels_binary)
        right_binary_lateralized += np.sum(right_voxels_binary > left_voxels_binary)
        total_binary_voxels += np.sum(left_voxels_binary | right_voxels_binary)
    
    # Calculate Binary Lateralization Index (LS_binary)
    if total_binary_voxels > 0:
        left_LI_binary = left_binary_lateralized / total_binary_voxels
        right_LI_binary = right_binary_lateralized / total_binary_voxels
        LS_binary = abs(left_binary_lateralized-right_binary_lateralized) / (left_binary_lateralized+right_binary_lateralized)
    else:
        left_LI_binary = 0
        right_LI_binary = 0
        LS_binary = 0

    if left_LI_binary > right_LI_binary: hempisphere = 'Left'
    elif left_LI_binary < right_LI_binary: hempisphere = 'Right'
    elif left_LI_binary == 0 and right_LI_binary == 0: hempisphere = 'No Side'
    else: hempisphere = 'Bilateral'
    
    return {
        "Left Binary Lateralization": round(left_LI_binary,3),
        "Right Binary Lateralization": round(right_LI_binary,3),
        "Lateralization Strength": round(LS_binary,3),
        "Side": hempisphere
    }