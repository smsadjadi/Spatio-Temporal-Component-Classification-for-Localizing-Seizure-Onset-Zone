# ===================================================================================================================
# Post-surgical MRI ================================================================================================
# ===================================================================================================================

# Directories =======================================================================================================
DATASET="/mnt/d/Academic/Datasets/Epilepsy_rsfMRI_Fallahi"
SUBJECTS=("Sub001" "Sub002" "Sub003" "Sub004" "Sub005" "Sub006" "Sub007" "Sub008" "Sub009" "Sub010")
for SUBJECT in "${SUBJECTS[@]}"; do

# Subject Data ======================================================================================================
echo
echo "----- Analysis of ${SUBJECT} -----"
echo

# Second STR to MNI Hr Transformation and Registration ==============================================================
echo "Running FLIRT registration: 2nd structural brain to MNI152 1mm template..."
if [ ! -f "${DATASET}/${SUBJECT}/post_t1/post_t1_normalized_hr.nii.gz" ]; then
flirt   -in ${DATASET}/${SUBJECT}/post_t1/post_t1 \
        -ref /home/smsadjadi/fsl/data/standard/MNI152_T1_1mm \
        -out ${DATASET}/${SUBJECT}/post_t1/post_t1_normalized_hr \
        -omat ${DATASET}/${SUBJECT}/regmats/poststr2mnihr.mat \
        -dof 7 \
        -cost mutualinfo
fi
POST2MNIhr="${DATASET}/${SUBJECT}/regmats/poststr2mnihr.mat"
POSThr_DIR="${DATASET}/${SUBJECT}/post_t1/post_t1_normalized_hr"

# Second STR to MNI Lr Transformation and Registration ==============================================================
echo "Running FLIRT registration: 2nd structural brain to MNI152 2mm template..."
if [ ! -f "${DATASET}/${SUBJECT}/post_t1/post_t1_normalized_lr.nii.gz" ]; then
flirt   -in ${DATASET}/${SUBJECT}/post_t1/post_t1_normalized_hr \
        -ref /home/smsadjadi/fsl/data/standard/MNI152_T1_2mm \
        -out ${DATASET}/${SUBJECT}/post_t1/post_t1_normalized_lr \
        -omat ${DATASET}/${SUBJECT}/regmats/mnihr2mnilr.mat \
        -dof 6 \
        -cost mutualinfo
fi
MNIhr2MNIlr="${DATASET}/${SUBJECT}/regmats/mnihr2mnilr.mat"
POSTlr_DIR="${DATASET}/${SUBJECT}/post_t1/post_t1_normalized_lr"

# Finish ============================================================================================================
echo "${SUBJECT} Finished!"

done
echo