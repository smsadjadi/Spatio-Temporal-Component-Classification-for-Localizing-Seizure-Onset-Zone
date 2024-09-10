from scipy.stats import pearsonr
import numpy as np

def lateralization_index(IC_matrix):
# Ensure the input is of the correct shape
    if IC_matrix.shape != (91, 109, 91):
        raise ValueError("IC_matrix must be of shape (91, 109, 91)")

    # Define the ACPC plane (mid-sagittal plane)
    mid_plane_index = 45  # This is the zero-based index for the mid-sagittal plane

    left_voxels = []
    right_voxels = []
    
    # Extract mirroring voxels from both sides of the brain
    for x in range(mid_plane_index):
        mirrored_x = IC_matrix.shape[0] - 1 - x  # Find the mirroring voxel
        right_voxels.append(IC_matrix[x, :, :])
        left_voxels.append(IC_matrix[mirrored_x, :, :])
    
    # Flatten the voxel arrays
    left_voxels = np.array(left_voxels).flatten()
    right_voxels = np.array(right_voxels).flatten()
    
    # Calculate Pearson's correlation coefficient (symmetricity)
    correlation, _ = pearsonr(left_voxels, right_voxels)
    
    # Calculate mean and standard deviation of symmetricity
    symmetricities = [correlation]  # In a more complex scenario, you might have multiple ICs
    mean_symmetricity = np.mean(symmetricities)
    std_symmetricity = np.std(symmetricities)
    
    # Determine cut-off for symmetricity
    cutoff = 1 # mean_symmetricity - std_symmetricity
    
    # Filter out components with symmetricity greater than the cut-off
    if correlation <= cutoff:
        # Calculate Lateralization Index (LI)
        LI = np.float(1 - np.abs(correlation))
        return {"Lateralization Index": round(LI,3), "Symmetricity": round(correlation,3)}
    else:
        return {"Lateralization Index": None, "Symmetricity": round(correlation,3)}
