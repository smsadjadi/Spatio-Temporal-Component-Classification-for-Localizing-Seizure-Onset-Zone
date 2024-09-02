import nibabel as nib

def nifti_save(array,affine,dir,name):
    
    nifti_array = nib.Nifti1Image(array, affine)
    nib.save(nifti_array,dir+'\\'+name+'.nii.gz')
    
    print('')
    print (f'{name}.nii.gz > saved!')