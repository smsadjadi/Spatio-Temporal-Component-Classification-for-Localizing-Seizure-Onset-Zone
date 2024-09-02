import numpy as np

def slice_timing_to_order(slice_timing):
    slice_order = np.argsort(slice_timing) + 1  # +1 for 1-based indexing
    return slice_order