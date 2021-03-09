#!/bin/bash

# Getting input as to which lite version the model should be converted to.
echo "Which version of lite model do you want to convert the model into?"
echo "(1) float16; (2) int16; (3) int8"
read LITE_MODEL

echo $LITE_MODEL
LITE_MODEL_PARAM=""
if [[ $LITE_MODEL -eq 1 ]];
then
  LITE_MODEL_PARAM="ctranslate2_float16"
elif [[ $LITE_MODEL -eq 2 ]];
then
  LITE_MODEL_PARAM="ctranslate2_int16"
elif [[ $LITE_MODEL -eq 3 ]];
then
  LITE_MODEL_PARAM="ctranslate2_int8"
else
  echo "Wrong param, please choose (1), (2), or (3)."
  exit 2
fi

# Construct date path.
DATE=$(date +"%Y_%m_%d_%H_%M")
EXPORT_DIR="tf_lite_export_${DATE}"
echo "Outputting the lite model to dir: $EXPORT_DIR"

# Convert the model into a lite version
onmt-main --config run_aslg.yml export --export_dir "$EXPORT_DIR" --export_format "$LITE_MODEL_PARAM"