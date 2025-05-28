#! /bin/sh
set -e

OUTPUT_FILE='./_test.py'
ACCOUNT=$1
ENDPOINT=$2
API_KEY=$3

for f in $(find ./docs/extras/code_samples -maxdepth 1 -name "*.txt" -not -name "workflow_*.txt" | sort -h)
do
  echo
  echo "###############################################"
  echo "${f}"
  echo "###############################################"
  echo

  sed "s/my-api-key/${API_KEY}/" "${f}" > $OUTPUT_FILE
  sed -i 's/\/path\/to\/the\/file.ext/.\/tests\/data\/file_types\/pdf\/blank_1.pdf/' $OUTPUT_FILE

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
