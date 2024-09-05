# ===================================================================================================================
# Pre-surgical Data =================================================================================================
# ===================================================================================================================

# Directories =======================================================================================================
DATASET="/mnt/d/Academic/Datasets/Epilepsy_rsfMRI_Fallahi"
MNI_LR="/home/smsadjadi/fsl/data/standard/MNI152_T1_2mm_brain"
MNI_HR="/home/smsadjadi/fsl/data/standard/MNI152_T1_1mm"
DESIGN="${DATASET}/Archive/Design"
if [ ! -d "$DESIGN/modified" ]; then mkdir $DESIGN/modified; fi

SUBJECTS=("Sub001" "Sub002" "Sub003" "Sub004" "Sub005" "Sub006" "Sub007" "Sub008" "Sub009" "Sub010")
for SUBJECT in "${SUBJECTS[@]}"; do

# Subject Data ======================================================================================================
echo
echo "----- Analysis of ${SUBJECT} -----"
echo
BOLD_DIR="${DATASET}/${SUBJECT}/pre_bold/pre_bold"
T1_DIR="${DATASET}/${SUBJECT}/pre_t1/pre_t1"
if [ ! -d "${DATASET}/${SUBJECT}/regmats" ]; then mkdir ${DATASET}/${SUBJECT}/regmats; fi

# BOLD Preprocessing ================================================================================================
echo "Running initial FEAT preprocessing..."
if [ ! -f "${DATASET}/${SUBJECT}/pre_bold/pre_bold.feat/mean_func.nii.gz" ]; then
rm -rf "${DATASET}/${SUBJECT}/pre_bold/pre_bold.feat"
FSF_TEMPLATE="${DESIGN}/s1_feat_preprocessing.fsf"
FSF_MODIFIED="${DESIGN}/modified/${SUBJECT}_feat_preprocessing.fsf"
sed "s|INPUT_PATH|${BOLD_DIR}|g" $FSF_TEMPLATE > $FSF_MODIFIED
feat $FSF_MODIFIED
fi
BOLD_DIR="${DATASET}/${SUBJECT}/pre_bold/pre_bold.feat/filtered_func_data"
BOLD_MEAN="${DATASET}/${SUBJECT}/pre_bold/pre_bold.feat/mean_func"

# STR Brain Extraction ==============================================================================================
echo "Running BET brain extraction on structural data..."
if [ ! -f "${DATASET}/${SUBJECT}/pre_t1/pre_t1_brain.nii.gz" ]; then
bet ${T1_DIR} ${T1_DIR}_brain -f 0.5 -g 0 -m
fi
T1_DIR="${DATASET}/${SUBJECT}/pre_t1/pre_t1_brain"

# BOLD to STR Transformation ========================================================================================
echo "Running FLIRT registration: functional to structural brain image..."
if [ ! -f "${DATASET}/${SUBJECT}/regmats/func2prestr.mat" ]; then
flirt   -in ${BOLD_MEAN} \
        -ref ${T1_DIR} \
        -omat ${DATASET}/${SUBJECT}/regmats/func2prestr.mat \
        -dof 12 -searchrx -180 180 -searchry -180 180 -searchrz -180 180
fi
FUNC2STR="${DATASET}/${SUBJECT}/regmats/func2prestr.mat"

# STR to MNI Lr Transformation and Registration =====================================================================
echo "Running FLIRT registration: structural brain to MNI152 template..." # applywarp instead of flirt if nonlinear
if [ ! -f "${DATASET}/${SUBJECT}/pre_t1/pre_t1_brain_normalized_lr.nii.gz" ]; then
flirt   -in ${T1_DIR} \
        -ref ${MNI_LR} \
        -out ${T1_DIR}_normalized_lr \
        -omat ${DATASET}/${SUBJECT}/regmats/prestr2mnilr.mat \
        -dof 12
fi
STR2MNIlr="${DATASET}/${SUBJECT}/regmats/prestr2mnilr.mat"
T1_DIR="${DATASET}/${SUBJECT}/pre_t1/pre_t1_brain_normalized_lr"

# STR Mask to MNI Lr Transformation and Registration =====================================================================
echo "Running FLIRT registration: structural brain mask to MNI152 template..."
if [ ! -f "${DATASET}/${SUBJECT}/pre_t1/pre_t1_brain_mask_normalized_lr.nii.gz" ]; then
flirt   -in ${DATASET}/${SUBJECT}/pre_t1/pre_t1_brain_mask \
        -ref ${MNI_LR} \
        -out ${DATASET}/${SUBJECT}/pre_t1/pre_t1_brain_mask_normalized_lr \
        -omat ${DATASET}/${SUBJECT}/regmats/premask2mnilr.mat \
        -dof 7 \
        -cost mutualinfo
fi
MASK2MNIlr="${DATASET}/${SUBJECT}/regmats/premask2mnilr.mat"

# STR to MNI Hr Transformation and Registration =====================================================================
echo "Running FLIRT registration: structural to MNI152 1mm template..."
if [ ! -f "${DATASET}/${SUBJECT}/pre_t1/pre_t1_normalized_hr.nii.gz" ]; then
flirt   -in ${DATASET}/${SUBJECT}/pre_t1/pre_t1 \
        -ref ${MNI_HR} \
        -out ${DATASET}/${SUBJECT}/pre_t1/pre_t1_normalized_hr \
        -omat ${DATASET}/${SUBJECT}/regmats/prestr2mnihr.mat \
        -dof 7 \
        -cost mutualinfo
fi
PRE2MNIhr="${DATASET}/${SUBJECT}/regmats/prestr2mnihr.mat"
PREhr_DIR="${DATASET}/${SUBJECT}/pre_t1/pre_t1_normalized_hr"

# BOLD to MNI Transformation ========================================================================================
echo "Concatenating transformations..."
if [ ! -f "${DATASET}/${SUBJECT}/regmats/func2mnilr.mat" ]; then
convert_xfm -concat ${STR2MNIlr} ${FUNC2STR} -omat ${DATASET}/${SUBJECT}/regmats/func2mnilr.mat
fi
FUNC2MNIlr="${DATASET}/${SUBJECT}/regmats/func2mnilr.mat"

# BOLD to MNI Normalization =========================================================================================
echo "Running FLIRT registration: functional to MNI152 template..."
if [ ! -f "${DATASET}/${SUBJECT}/pre_bold/pre_bold_preprocessed.nii.gz" ]; then
flirt   -in ${BOLD_DIR} \
        -ref ${MNI_LR} \
        -applyxfm -init ${FUNC2MNIlr} \
        -out ${DATASET}/${SUBJECT}/pre_bold/pre_bold_preprocessed
fi
BOLD_DIR="${DATASET}/${SUBJECT}/pre_bold/pre_bold_preprocessed"

# BOLD_MASK =========================================================================================================
echo "Creating mask of the preprocessed functional data..."
if [ ! -f "${DATASET}/${SUBJECT}/pre_bold/pre_bold_preprocessed_mask.nii.gz" ]; then
fslmaths ${BOLD_DIR} -bin ${BOLD_DIR}_mask
fi
BOLD_MASK="${DATASET}/${SUBJECT}/pre_bold/pre_bold_preprocessed_mask"

# FEAT for MELODIC ICA ==============================================================================================
echo "Running FEAT MELODIC ICA..."
if [ ! -f "${DATASET}/${SUBJECT}/pre_bold/pre_bold_preprocessed.ica/filtered_func_data.ica/melodic_IC.nii.gz" ]; then
rm -rf "${DATASET}/${SUBJECT}/pre_bold/pre_bold_preprocessed.ica"
FSF_TEMPLATE="${DESIGN}/s2_melodic_ica.fsf"
FSF_MODIFIED="${DESIGN}/modified/${SUBJECT}_melodic_ica.fsf"
sed "s|INPUT_PATH|${BOLD_DIR}|g" $FSF_TEMPLATE > $FSF_MODIFIED
feat $FSF_MODIFIED
fi
MELODIC_IC="${DATASET}/${SUBJECT}/pre_bold/pre_bold_preprocessed.ica/filtered_func_data.ica/melodic_IC"

# Finish ============================================================================================================
# rm -rf "${DATASET}/${SUBJECT}/pre_bold/pre_bold.feat"
echo "${SUBJECT} Finished!"

done
echo