# Directories =======================================================================================================
DATASET="/mnt/d/Academic/Datasets/Epilepsy_rsfMRI_Fallahi"
MNI_TEMPLATE="/home/smsadjadi/fsl/data/standard/MNI152_T1_2mm_brain"
DESIGN="${DATASET}/Archive/Design"
if [ ! -d "$DESIGN/modified" ]; mkdir $DESIGN/modified; fi
SUBJECTS=("Sub001" "Sub002" "Sub003" "Sub004" "Sub005" "Sub006" "Sub007" "Sub008" "Sub009" "Sub010")

for SUBJECT in "${SUBJECTS[@]}"; do

# Subject Data ======================================================================================================
echo
echo "----- Analysis of ${SUBJECT} -----"
echo
BOLD_DIR="${DATASET}/${SUBJECT}/pre_bold/pre_bold"
T1_DIR="${DATASET}/${SUBJECT}/pre_t1/pre_t1"

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
bet ${T1_DIR} ${T1_DIR}_brain -f 0.5 -g 0
fi
T1_DIR="${DATASET}/${SUBJECT}/pre_t1/pre_t1_brain"

# BOLD to STR Transformation ========================================================================================
echo "Running FLIRT registration: functional to structural brain image..."
if [ ! -f "${DATASET}/${SUBJECT}/func2prestr.mat" ]; then
flirt   -in ${BOLD_MEAN} \
        -ref ${T1_DIR} \
        -omat ${DATASET}/${SUBJECT}/func2prestr.mat \
        -dof 12 -searchrx -180 180 -searchry -180 180 -searchrz -180 180
fi
FUNC2STR="${DATASET}/${SUBJECT}/func2prestr.mat"

# STR to MNI Transformation and Registration ========================================================================
echo "Running FLIRT registration: structural brain to MNI152 template..."
if [ ! -f "${DATASET}/${SUBJECT}/pre_t1/pre_t1_brain_normalized.nii.gz" ]; then
flirt   -in ${T1_DIR} \
        -ref ${MNI_TEMPLATE} \
        -out ${T1_DIR}_normalized \
        -omat ${DATASET}/${SUBJECT}/prestr2mni.mat \
        -dof 12
fi
STR2MNI="${DATASET}/${SUBJECT}/prestr2mni.mat"
T1_DIR="${DATASET}/${SUBJECT}/pre_t1/pre_t1_brain_normalized"

# BOLD to MNI Transformation ========================================================================================
echo "Concatenating transformations..."
if [ ! -f "${DATASET}/${SUBJECT}/func2mni.mat" ]; then
convert_xfm -concat ${STR2MNI} ${FUNC2STR} -omat ${DATASET}/${SUBJECT}/func2mni.mat
fi
FUNC2MNI="${DATASET}/${SUBJECT}/func2mni.mat"

# BOLD to MNI Normalization =========================================================================================
echo "Running FLIRT registration: functional to MNI152 template..."
if [ ! -f "${DATASET}/${SUBJECT}/pre_bold/pre_bold_preprocessed.nii.gz" ]; then
flirt   -in ${BOLD_DIR} \
        -ref ${MNI_TEMPLATE} \
        -applyxfm -init ${FUNC2MNI} \
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

# Second STR to MNI Transformation and Registration =================================================================
echo "Running FLIRT registration: 2nd structural brain to MNI152 template..."
if [ ! -f "${DATASET}/${SUBJECT}/post_t1/post_t1_normalized.nii.gz" ]; then
flirt   -in ${DATASET}/${SUBJECT}/post_t1/post_t1 \
        -ref /home/smsadjadi/fsl/data/standard/MNI152_T1_1mm \
        -out ${DATASET}/${SUBJECT}/post_t1/post_t1_normalized \
        -omat ${DATASET}/${SUBJECT}/poststr2mni.mat \
        -dof 7 \
        -cost mutualinfo
fi
POST2MNI="${DATASET}/${SUBJECT}/poststr2mni.mat"
POST_DIR="${DATASET}/${SUBJECT}/post_t1/post_t1_normalized"

# Finish ============================================================================================================
# rm -rf "${DATASET}/${SUBJECT}/pre_bold/pre_bold.feat"
echo "${SUBJECT} Finished!"

done
echo