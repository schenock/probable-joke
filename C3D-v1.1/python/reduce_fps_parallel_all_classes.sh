INPUT_FOLDER=$1
OUTPUT_FOLDER=$2

for f in `ls $INPUT_FOLDER`;
do
  mkdir $OUTPUT_FOLDER/$f
  for i in `ls $INPUT_FOLDER/$f`;
  do
    mkdir $OUTPUT_FOLDER/$f/$i
    python reduce_fps_parallel.py $INPUT_FOLDER/$f/$i $OUTPUT_FOLDER/$f/$i 7.5
  done
done