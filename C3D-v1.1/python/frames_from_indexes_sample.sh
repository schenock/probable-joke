INPUT_FOLDER=$1
ALIGN_IDX_FOLDER=$2
OUTPUT_FOLDER=$3

for CLASS in {01..43};
do
    echo "For sample class: " $CLASS
    echo

    for SAMPLE_FOLDER in `ls $ALIGN_IDX_FOLDER/$CLASS`
    do
        echo -e "\tFor sample folder: " $SAMPLE_FOLDER
        echo

        for align_file in `ls $ALIGN_IDX_FOLDER/$CLASS`
        do
            echo -e "\t\tCreating video for: " $alignment_file " in " $SAMPLE_FOLDER
            echo

            VID_INPUT_FOLDER=$INPUT_FOLDER/$SAMPLE_FOLDER
            VID_ALIGN_FILE=$ALIGN_IDX_FOLDER/$CLASS/$align_file
            VID_OUTPUT_FOLDER=$OUTPUT_FOLDER/$SAMPLE_FOLDER/

            echo -e "\t\tCreating output folder: " $VID_OUTPUT_FOLDER
            mkdir -p $VID_OUTPUT_FOLDER

            python frames_from_indexes_sample.py $VID_INPUT_FOLDER $VID_ALIGN_FILE $VID_OUTPUT_FOLDER
        done 
    done
done