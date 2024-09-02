import nibabel as nib

def ic_extract(data,candidate_ic):
    ic = data.get_fdata()[:,:,:,candidate_ic-1]
    return ic
    