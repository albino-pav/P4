#!/bin/bash

#In order to call this script, we go to PAV/P4 and introduce the following:  
#scripts/locutor_pearson.sh
    #You'll obtain the pearson for all files of a locutor, each file separated 
    #by a long line that indicates the path of the file. 

#Directory of the chosen LOCUTOR
DIR=$(pwd)"/spk_8mu/speecon/BLOCK01/SES014/*.wav"
#LOCUTOR=${DIR##*/} #SES014

for FILE in $DIR; do
#define outputfiles names 
P=${FILE##*/}
echo $FILE
SES=${P%.*}
FILELP="salida_pearson_$SES.lp"
FILELPC="salida_pearson_$SES.lpcc"
FILEMPCC="salida_pearson_$SES.mfcc"

#Create files for pearson processing 
wav2lp 12 $FILE $FILELP
#wav2lpcc 12 12 $FILE $FILELPC
#wav2mfcc 12 $FILE $FILEMFCC

#process with pearson
pearson $FILELP
#pearson $FILELPC
#cdpearson $FILEMFCC
done
