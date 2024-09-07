# ===================================================================================================================
# Resulting Data ====================================================================================================
# ===================================================================================================================

# Directories =======================================================================================================
DATASET="/mnt/d/Academic/Datasets/Epilepsy_rsfMRI_Fallahi"
SUBJECTS=("Sub001" "Sub002" "Sub003" "Sub004" "Sub005" "Sub006" "Sub007" "Sub008" "Sub009" "Sub010")
for SUBJECT in "${SUBJECTS[@]}"; do

# Subject Data ======================================================================================================
echo
echo "----- Analysis of ${SUBJECT} -----"
echo

# Second STR MNI Lr to MNI Hr Transformation ========================================================================
echo "Inversing transformations from MNI152 2mm to MNI152 1mm template..."
if [ ! -f "${DATASET}/${SUBJECT}/regmats/mnilr2mnihr.mat" ]; then
convert_xfm -inverse ${DATASET}/${SUBJECT}/regmats/mnihr2mnilr.mat -omat ${DATASET}/${SUBJECT}/regmats/mnilr2mnihr.mat
fi
MNIlr2MNIhr="${DATASET}/${SUBJECT}/regmats/mnilr2mnihr.mat"

# Resulting EZ Area to MNI Hr Transformation ========================================================================
echo "Running FLIRT registration: resulting ez area to MNI152 1mm template..."
if [ -f "${DATASET}/${SUBJECT}/pre_bold/pre_bold_preprocessed.ica/filtered_func_data.ica/ez_area.nii.gz" ] && \
[ ! -f "${DATASET}/${SUBJECT}/pre_bold/pre_bold_preprocessed.ica/filtered_func_data.ica/ez_area_hr.nii.gz" ]; then
flirt   -in ${DATASET}/${SUBJECT}/pre_bold/pre_bold_preprocessed.ica/filtered_func_data.ica/ez_area \
        -ref /home/smsadjadi/fsl/data/standard/MNI152_T1_1mm \
        -applyxfm \
        -init ${MNIlr2MNIhr} \
        -out ${DATASET}/${SUBJECT}/pre_bold/pre_bold_preprocessed.ica/filtered_func_data.ica/ez_area_hr
fi
EZAREAhr="${DATASET}/${SUBJECT}/pre_bold/pre_bold_preprocessed.ica/filtered_func_data.ica/ez_area_hr"

# Finish ============================================================================================================
echo "${SUBJECT} Finished!"

done
echo