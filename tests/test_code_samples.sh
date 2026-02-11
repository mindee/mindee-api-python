#! /bin/sh
set -e

OUTPUT_FILE='./_test.py'
ACCOUNT=$1
ENDPOINT=$2
API_KEY=$3
API_KEY_V2=$4
MODEL_ID=$5
CLASSIFICATION_MODEL_ID=$6
CROP_MODEL_ID=$7
OCR_MODEL_ID=$8
SPLIT_MODEL_ID=$9

for f in $(find ./docs/extras/code_samples -maxdepth 1 -name "*.txt" -not -name "workflow_*.txt" | sort -h)
do
  if echo "${f}" | grep -q "default_v2.txt"; then
    if [ -z "${API_KEY_V2}" ] || [ -z "${MODEL_ID}" ]; then
      echo "Skipping ${f} (API_KEY_V2 or MODEL_ID not supplied)"
      echo
      continue
    fi
  fi

  echo
  echo "###############################################"
  echo "${f}"
  echo "###############################################"
  echo

  sed "s/my-api-key/${API_KEY}/" "${f}" > $OUTPUT_FILE
  sed -i 's/\/path\/to\/the\/file.ext/.\/tests\/data\/file_types\/pdf\/blank_1.pdf/' $OUTPUT_FILE


  if echo "${f}" | grep -q "v2_extraction.txt"
  then
    sed -i "s/MY_API_KEY/$API_KEY_V2/" $OUTPUT_FILE
    sed -i "s/MY_MODEL_ID/$MODEL_ID/" $OUTPUT_FILE
  else
    sed -i "s/my-api-key/$API_KEY/" $OUTPUT_FILE
  fi

  if echo "${f}" | grep -q "v2_classification.txt"
  then
    sed -i "s/MY_API_KEY/$API_KEY_V2/" $OUTPUT_FILE
    sed -i "s/MY_CLASSIFICATION_MODEL_ID/$CLASSIFICATION_MODEL_ID/" $OUTPUT_FILE
  else
    sed -i "s/my-api-key/$API_KEY/" $OUTPUT_FILE
  fi

  if echo "${f}" | grep -q "v2_crop.txt"
  then
    sed -i "s/MY_API_KEY/$API_KEY_V2/" $OUTPUT_FILE
    sed -i "s/MY_CROP_MODEL_ID/$CROP_MODEL_ID/" $OUTPUT_FILE
  else
    sed -i "s/my-api-key/$API_KEY/" $OUTPUT_FILE
  fi

  if echo "${f}" | grep -q "v2_split.txt"
  then
    sed -i "s/MY_API_KEY/$API_KEY_V2/" $OUTPUT_FILE
    sed -i "s/MY_SPLIT_MODEL_ID/$SPLIT_MODEL_ID/" $OUTPUT_FILE
  else
    sed -i "s/my-api-key/$API_KEY/" $OUTPUT_FILE
  fi

  if echo "${f}" | grep -q "v2_ocr.txt"
  then
    sed -i "s/MY_API_KEY/$API_KEY_V2/" $OUTPUT_FILE
    sed -i "s/MY_OCR_MODEL_ID/$OCR_MODEL_ID/" $OUTPUT_FILE
  else
    sed -i "s/my-api-key/$API_KEY/" $OUTPUT_FILE
  fi

  if echo "$f" | grep -q "custom_v1.txt"
  then
    sed -i "s/my-account/$ACCOUNT/g" $OUTPUT_FILE
    sed -i "s/my-endpoint/$ENDPOINT/g" $OUTPUT_FILE
  fi

  if echo "${f}" | grep -q "default.txt"
  then
    sed -i "s/my-account/$ACCOUNT/" $OUTPUT_FILE
    sed -i "s/my-endpoint/$ENDPOINT/" $OUTPUT_FILE
    sed -i "s/my-version/1/" $OUTPUT_FILE
  fi

  if echo "${f}" | grep -q "default_async.txt"
  then
    sed -i "s/my-account/mindee/" $OUTPUT_FILE
    sed -i "s/my-endpoint/invoice_splitter/" $OUTPUT_FILE
    sed -i "s/my-version/1/" $OUTPUT_FILE
  fi

  python $OUTPUT_FILE
done
