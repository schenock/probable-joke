#!/usr/bin/env bash

INPUT_FOLDER=$1
CLASS=$2
TEST_SAMPLE=$3
OUTPUT_FOLDER=$4

ENR_CODE=`dirname $0`  # Current folder

source ${ENR_CODE}/../config.sh

CMD="\
    addpath(genpath([cd '/' '$ENR_CODE'])); \
    align_deep_pca_gctw_class_test('${INPUT_FOLDER}/${CLASS}', '$CLASS', '$TEST_SAMPLE', '$OUTPUT_FOLDER', '$ENR_CODE'); \
    exit;
"

$MATLAB -r "$CMD" # > gctw.log 2>&1


