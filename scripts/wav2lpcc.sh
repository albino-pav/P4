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
<<<<<<< HEAD
   echo "$0 lpc_order input.wav output.lpcc"
=======
   echo "$0 lpc_order cepstrum_order input.wav output.lp"
>>>>>>> c1de2e004711e8f0cdc88483746960d663e0ac61
   exit 1
fi

lpc_order=$1
cepstrum_order=$2 #GOOD VALUE = 13 
inputfile=$3
outputfile=$4

UBUNTU_SPTK=1
if [[ $UBUNTU_SPTK == 1 ]]; then
   # In case you install SPTK using debian package (apt-get)
   X2X="sptk x2x"
   FRAME="sptk frame"
   WINDOW="sptk window"
   LPC="sptk lpc"
   LPC2C = "sptk lpc2c"
else
   # or install SPTK building it from its source
   X2X="x2x"
   FRAME="frame"
   WINDOW="window"
   LPC="lpc"
   LPC2C = "lpc2c"
fi

# Main command for feature extration
sox $inputfile -t raw -e signed -b 16 - | #convert (-t) wav file to raw file 
                                          #encode (-e) as signed with 16b
    $X2X +sf |                            #convert from short to float (4bytes)
    $FRAME -l 240 -p 80 |                 #divide la señal en tramas de 240 muestras
                                          #con desplazamiento de 80 muestras
    $WINDOW -l 240 -L 240 |               #enventana con Blackman longitud 240
                                          #-l frame length input, -L frame length output
	$LPC -l 240 -m $lpc_order |           #calculates lpc  of -l length framed windowed data
                                          #performs order -m LPC 
   $LPC2C -m $lpc_order -M $cepstrum_order > $base.cep  #computes LPC cepstral coeffs from LPC

# Our array files need a header with the number of cols and rows:
#Esto se hace para que haga match con el formato fmatrix
ncol=$((cepstrum_order)) #gives cepstrum_order coefficients as output 
#El numero de filas = numero de tramas
   #convierte el asci leido de base.cep a float 
   #el resultado lo pasa a wc -l, que cuenta las lineas que hay en el fichero
   #perl -ne es un while que recorre lineas y te printea en el fichero base.cep
      #el número correspondiente para cada    

nrow=`$X2X +fa < $base.cep | wc -l | perl -ne 'print $_/'$ncol', "\n";'`

# Build fmatrix file by placing nrow and ncol in front, and the data after them
#x2x +aI conversión de auscii a unsigned int (4bytes) de los valores de fila y columna
echo $nrow $ncol | $X2X +aI > $outputfile
# cat - Copy standard input to standard output.-> copia el fichero base.cep
   #al final de outputfile (<<) sin cambiar nada. 
cat $base.cep >> $outputfile

exit
