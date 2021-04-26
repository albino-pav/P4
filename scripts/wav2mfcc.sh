#!/bin/bash

## \file
## \TODO This file implements a very trivial feature extraction; use it as a template for other front ends.
## 
## Please, read SPTK documentation and some papers in order to implement more advanced front ends.

# Base name for temporary files
base=/tmp/$(basename $0).$$ # $0 es el directorio del script / basename coge el fichero y elimina el directorio / $$ es el numero de proceso

# Ensure cleanup of temporary files on exit
trap cleanup EXIT # truco que elimina el fichero temporal si o si
cleanup() {
   \rm -f $base.*
}

if [[ $# != 3 ]]; then # 
   echo "$0 lpc_order input.wav output.lp"
   exit 1
fi

mfcc_order=$1 # orden del analisis
inputfile=$2
outputfile=$3

# UBUNTU_SPTK=0 # los de mac tenemos que poner 0
if [[ $UBUNTU_SPTK == 1 ]]; then
   # In case you install SPTK using debian package (apt-get)
   X2X="sptk x2x"
   FRAME="sptk frame"
   WINDOW="sptk window"
   MFCC="sptk mfcc"
else
   # or install SPTK building it from its source
   X2X="x2x"
   FRAME="frame"
   WINDOW="window"
   MFCC="mfcc"
fi

# Main command for feature extration 
sox $inputfile -t raw -e signed -b 16 - | $X2X +sf | $FRAME -l 240 -p 80 | $WINDOW -l 240 -L 240 |
	$MFCC -l 240 -m $mfcc_order -s 8 -w 1 -n 40 > $base.mfcc
# Sin ventana (-w 1) y con 40 Mel-filters (-n 40)

# Our array files need a header with the number of cols and rows:
ncol=$((mfcc_order+1)) # lpc p =>  (gain a1 a2 ... ap) 
nrow=`$X2X +fa < $base.mfcc | wc -l | perl -ne 'print $_/'$ncol', "\n";'`

# Build fmatrix file by placing nrow and ncol in front, and the data after them
echo $nrow $ncol | $X2X +aI > $outputfile
cat $base.mfcc >> $outputfile

exit
