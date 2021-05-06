#!/bin/bash

## \file
## \TODO This file implements a very trivial feature extraction; use it as a template for other front ends.
## 
## Please, read SPTK documentation and some papers in order to implement more advanced front ends.

# Base name for temporary files
   #basename te da el nombre del fichero con su extensión
   #$0 te indica que el fichero sobre el que quieres ejecutar basename es el actual
base=/tmp/$(basename $0).$$ 

# Ensure cleanup of temporary files on exit
trap cleanup EXIT #trap hace que se ejecute cleanup siempre que termine la ejecución
                  #sin importar en qué punto ha terminado. 
cleanup() {
   \rm -f $base.*
}

if [[ $# != 3 ]]; then
   echo "$0 lpc_order input.wav output.lp"
   exit 1
fi

lpc_order=$1 #GOOD VALUE = 12
inputfile=$2
outputfile=$3

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
fi

# Main command for feature extration
sox $inputfile -t raw -e signed -b 16 - | $X2X +sf | $FRAME -l 240 -p 80 | $WINDOW -l 240 -L 240 |
	$LPC -l 240 -m $lpc_order > $base.lp

# Our array files need a header with the number of cols and rows:
#Esto se hace para que haga match con el formato fmatrix
ncol=$((lpc_order+1)) # lpc p =>  (gain a1 a2 ... ap) - ganancia de predicción seguida de p coeficientes
 # (por ser una predicción lineal) 
#El numero de filas = numero de tramas
   #convierte el asci leido de base.lp a float 
   #el resultado lo pasa a wc -l, que cuenta las lineas que hay en el fichero
   #perl -ne es un while que recorre lineas y te printea en el fichero base.lp
      #el número correspondiente para cada    

nrow=`$X2X +fa < $base.lp | wc -l | perl -ne 'print $_/'$ncol', "\n";'`

# Build fmatrix file by placing nrow and ncol in front, and the data after them
#x2x +aI conversión de auscii a unsigned int (4bytes) de los valores de fila y columna
echo $nrow $ncol | $X2X +aI > $outputfile
# cat - Copy standard input to standard output.-> copia el fichero base.lp 
   #al final de outputfile (<<) sin cambiar nada. 
cat $base.lp >> $outputfile

exit
