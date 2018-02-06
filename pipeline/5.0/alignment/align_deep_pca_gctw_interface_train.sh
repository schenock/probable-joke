#!/usr/bin/env bash

INPUT_FOLDER=$1
OUTPUT_FOLDER=$2

MATLAB=/usr/local/bin/matlab2017a

> gctw.log

for i in {01..43};
do
    echo Aligning class $i
    echo Aligning class $i > gctw.log
    ENR_CODE=`dirname $0`  # Current folder

    CMD="\
        try; \
            addpath(genpath(['$ENR_CODE'])); \
            align_deep_pca_gctw_class_train('${INPUT_FOLDER}/${i}', '$i', '$OUTPUT_FOLDER', '$ENR_CODE'); \
        catch; \
        end; \
        exit;
    "

    $MATLAB -r "$CMD" >> gctw.log 2>&1

done