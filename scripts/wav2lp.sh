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

lpc_order=$1 # orden del analisis
inputfile=$2
outputfile=$3

# UBUNTU_SPTK=0 # los de mac tenemos que poner 0
if [[ $UBUNTU_SPTK == 1 ]]; then
   # In case you install SPTK using debian package (apt-get)
   X2X="sptk x2x"
   FRAME="sptk frame"
   WINDOW="sptk window"
   LPC="sptk lpc"
else
   # or install SPTK building it from its source
   X2X="x2x"
   FRAME="frame"
   WINDOW="window"
   LPC="lpc"
   LPCC="lpcc"
fi

# Main command for feature extration / 240 muestras son 30 ms, 80 muestras son 10 ms
sox $inputfile -t raw -e signed -b 16 - | $X2X +sf | $FRAME -l 240 -p 80 | $WINDOW -l 240 -L 240 |
	$LPC -l 240 -m $lpc_order > $base.lp

# Our array files need a header with the number of cols and rows:
ncol=$((lpc_order+1)) # lpc p =>  (gain a1 a2 ... ap) 
nrow=`$X2X +fa < $base.lp | wc -l | perl -ne 'print $_/'$ncol', "\n";'` # transforma de real a texto el fichero temporal, obtenemos el numero de tramas
# habran p+1*num_tramas filas; al dividir entre p+1 obtenemos num_tramas
# Build fmatrix file by placing nrow and ncol in front, and the data after them
echo $nrow $ncol | $X2X +aI > $outputfile # convertir de ascii a enteros de 4 bytes
cat $base.lp >> $outputfile # se añade a continuacion

exit
