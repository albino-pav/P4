PAV - P4: reconocimiento y verificación del locutor
===================================================

Obtenga su copia del repositorio de la práctica accediendo a [Práctica 4](https://github.com/albino-pav/P4)
y pulsando sobre el botón `Fork` situado en la esquina superior derecha. A continuación, siga las
instrucciones de la [Práctica 2](https://github.com/albino-pav/P2) para crear una rama con el apellido de
los integrantes del grupo de prácticas, dar de alta al resto de integrantes como colaboradores del proyecto
y crear la copias locales del repositorio.

También debe descomprimir, en el directorio `PAV/P4`, el fichero [db_8mu.tgz](https://atenea.upc.edu/pluginfile.php/3145524/mod_assign/introattachment/0/spk_8mu.tgz?forcedownload=1)
con la base de datos oral que se utilizará en la parte experimental de la práctica.

Como entrega deberá realizar un *pull request* con el contenido de su copia del repositorio. Recuerde
que los ficheros entregados deberán estar en condiciones de ser ejecutados con sólo ejecutar:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.sh
  make release
  run_spkid mfcc train test classerr verify verifyerr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Recuerde que, además de los trabajos indicados en esta parte básica, también deberá realizar un proyecto
de ampliación, del cual deberá subir una memoria explicativa a Atenea y los ficheros correspondientes al
repositorio de la práctica.

A modo de memoria de la parte básica, complete, en este mismo documento y usando el formato *markdown*, los
ejercicios indicados.

## Ejercicios.

### SPTK, Sox y los scripts de extracción de características.

- Analice el script `wav2lp.sh` y explique la misión de los distintos comandos involucrados en el *pipeline*
  principal (`sox`, `$X2X`, `$FRAME`, `$WINDOW` y `$LPC`). Explique el significado de cada una de las 
  opciones empleadas y de sus valores.
  
> Al abrir el script wa2lp.sh, nos encontramos con que antes de realizar la parametrización de una señal .wav, se eliminan los 
> ficheros temporales, si existiesen, asociados a la parametrización (en este caso a través del cálculo de los coeficientes de predición lineal LPC).
> Tambien un "usage" que nos indica como se ultiliza el script, y que este necesita de una señal .wav de entrada, y que devuelve un fichero salida.lp.
```c
# Ensure cleanup of temporary files on exit
trap cleanup EXIT
cleanup() {
   \rm -f $base.*
}

if [[ $# != 3 ]]; then
   echo "$0 lpc_order input.wav output.lp"
   exit 1
fi
```
> A continuación, se declaran aquellos parámetros que el usuario tendra que especificar en el momento que se invoque el script. En este caso los importantes son el número de coeficientes LPC que queremos que se calculen, y los ficheros de entrada y salida. Tanto $1 como $2 y $3 guardan en ellos los parámetros especificados en orden por consola ($0 no se usa ya que es el primer argumento de todos realmente es el propio nombre del script en este caso).
> Despues, dependiendo del valor de la variable de entorno UBUNTU_SPTK, se especifica como se invocan los comandos o programas del paquete de código abierto para procesado de señal de voz SPTK.
```c
lpc_order=$1
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

```
> Tras ya haber especificado los parámetros que el usuario tendra que especificar en la linea de comandos (o en otro script), se pasa a la función principal de wav2lp.sh. El pipeline principal, gracias a los programas especificados justo en el paso anterior, conseguimos una extracción de caracteristicas adecuada para nuestra señal. El pipeline principal es el siguiente: 
```c
# Main command for feature extration
sox $inputfile -t raw -e signed -b 16 - | $X2X +sf | $FRAME -l 240 -p 80 | $WINDOW -l 240 -L 240 |$LPC -l 240 -m $lpc_order > $base.lp
```
> Analicemos cada uno de los pasos en esta pipeline:
```c
sox $inputfile -t raw -e signed -b 16 - 
```
>La herramienta sox nos permite convertir la entrada que esta en formato de ley mu a enteros de 16 bits con signo. Este paso es primordial ya que los ficheros .wav estan >codificados con la ley mu pero el posterior paso de parametrización con SPTK solo es capaz de leer señales de float4.
```c
$X2X +sf
```
>En este paso es donde conseguimos convertir finalmente los datos del fichero de entrada a los deseados. Gracias al paso anterior esta en formato enteros con signo de 2 bytes (+s). Y ahora pasamos a float de 4 bytes (+f).
```c
$FRAME -l 240 -p 80
```
>Pasamos al entramado de la señal. El programa frame nos permite configurar la ventana de extración de datos de una secuencia. En este caso nos interesa escoger ventanas de >30ms, que con una frecuencia de muestreo de 8000Hz correspondería a una ventana de 240 muestras. Tambien configuramos un desplazamiento entre ventanas de 10ms, lo que >corresponde a 80 muestras.
```c
$WINDOW -l 240 -L 240
```
>Usamos el programa "window" para enventanar la señal. Primero especificamos el número de muestras que entra, que tal y como hemos configurado en el paso previo de la pipeline, >tienen que ser 240 muestras. Luego se especifica la longitud en muestras de lo que sale.
```c
$LPC -l 240 -m $lpc_order > $base.lp
```
>Y finalmente, pasamos a la parametrización perse. En ella se especifican el número de muestras y el número de coeficientes de predicción lineal que en este caso tal y como >hemos explicado antes, pasaremos como parámetro cuando invoquemos el script.

- Explique el procedimiento seguido para obtener un fichero de formato *fmatrix* a partir de los ficheros de
  salida de SPTK (líneas 45 a 47 del script `wav2lp.sh`).
  ```c
  # Our array files need a header with the number of cols and rows:
  ncol=$((lpc_order+1)) # lpc p =>  (gain a1 a2 ... ap) 
  nrow=`$X2X +fa < $base.lp | wc -l | perl -ne 'print $_/'$ncol', "\n";'`
  ```
>Para obtener el número de columnas de la matriz, simplemente lo definimos como el orden escogido del LPC que son el número de coeficientes, y luego tenemos en cuenta una      >unidad más ya que el primer valor de todos es la ganancia. 
>Para calcular el número de filas se usa el comando perl. 
>Primero pasamos el contenido de nuestro ficheros temporales los cuales son un conjunto de floats de 4 bytes concatenados a formato ASCII. Se genera asi un fichero con un valor ASCII en cada linea, que el comando "wc -l" se encargara de extraer el número de lineas. De esta manera tenemos el número de valores que tenía nuestro fichero temporal. Conociendo el número de columnas, simplemente se divide el número de datos totales por el de columnas para obtener asi el número de filas.

  * ¿Por qué es conveniente usar este formato (u otro parecido)? Tenga en cuenta cuál es el formato de
    entrada y cuál es el de resultado.
    
>Haber pasado de una señal de voz .wav codificada con ley mu de 8 bits a el formato fmatrix nos permite tener las señales ordenadas y caracterizadas por tramas y coeficientes. Cada fila corresponde a una trama de señal y cada columna a cada uno de los coeficientes con los que se ha parametrizado la trama. Tambien este formato permite manejar mucho más fácilmente los datos. Los programas "fmatrix_show" y "fmatrix_cut" permiten mostrar el contenido de estos ficheros y seleccionar columnas concretas de los mismos.

- Escriba el *pipeline* principal usado para calcular los coeficientes cepstrales de predicción lineal
  (LPCC) en su fichero <code>scripts/wav2lpcc.sh</code>:
  ```c
  # Main command for feature extration
  sox $inputfile -t raw -e signed -b 16 - | $X2X +sf | $FRAME -l 240 -p 80 | $WINDOW -l 240 -L 240 |$LPC -l 240 -m $lpc_order | $LPCC -m $lpc_order -M $lpcc_order > $base.lpcc
  ```
  >Vemos que la pipeline principal de la parametrización LPCC sigue la misma idea que la parametrización anterior. Con la diferencia de que hay que tener en cuenta que para encontrar los coeficientes cepstrales, hace falta previamente sacar los coeficientes de la predicción lineal. De ahi que antes de delegar los datos de la parametrización cepstral al fichero temporal .lpcc, se saquen previamente los coeficientes de predicción lineal con el comando "lpc".

- Escriba el *pipeline* principal usado para calcular los coeficientes cepstrales en escala Mel (MFCC) en su
  fichero <code>scripts/wav2mfcc.sh</code>:
  ```c
  sox $inputfile -t raw -e signed -b 16 - | $X2X +sf | $FRAME -l 240 -p 80 | $WINDOW -l 240 -L 240 |$MFCC -s $fm -l 240 -m $mfcc_order -n $melbank_order > $base.mfcc
  ```
  >De nuevo, la misma idea pero como ahora buscamos los coeficientes Mel-cepstrales usaremos el comando "mfcc". En el podremos especificar tanto el número de coeficientes, como el banco de filtros que usaremos.
  
### Extracción de características.

- Inserte una imagen mostrando la dependencia entre los coeficientes 2 y 3 de las tres parametrizaciones
  para todas las señales de un locutor.
  
  + Indique **todas** las órdenes necesarias para obtener las gráficas a partir de las señales 
    parametrizadas.
  + ¿Cuál de ellas le parece que contiene más información?

- Usando el programa <code>pearson</code>, obtenga los coeficientes de correlación normalizada entre los
  parámetros 2 y 3 para un locutor, y rellene la tabla siguiente con los valores obtenidos.
  
  >Usamos el programa pearson de la siguiente manera:
  ```c
  pearson -N work/lp/BLOCK01/SES010/*.lp >lp_pearson.txt
  pearson -N work/lpcc/BLOCK01/SES010/*.lpcc >lpcc_pearson.txt
  pearson -N work/mfcc/BLOCK01/SES010/*.mfcc >mfcc_pearson.txt
  ```
    
  >Consultamos entonces los ficheros generados, y de ahi extraemos el coeficiente de correlación Pearson.
  >Para los coeficientes de predicción lineal:
  >
  <img src="https://user-images.githubusercontent.com/79224893/120047553-26a31400-c015-11eb-88c5-227a211cbfb8.png" width="300">
  
  >Para los coeficientes cepstrales:
  >
  <img src="https://user-images.githubusercontent.com/79224893/120047563-2f93e580-c015-11eb-8bb2-aeb12bcdbffc.png" width="300">
  
  >Para los coeficientes Mel-cepstrales:
  >
  <img src="https://user-images.githubusercontent.com/79224893/120047595-433f4c00-c015-11eb-8def-4ce162485b4d.png" width="300">
  
  >Nos queda por lo tanto la siguiente tabla:

  |                        | LP            | LPCC         | MFCC          |
  |------------------------|:-------------:|:------------:|:-------------:|
  | &rho;<sub>x</sub>[2,3] |   -0.666745   |   0.334289   |   0.0588095   |
  
  + Compare los resultados de <code>pearson</code> con los obtenidos gráficamente.
  
  > Como podemos apreciar, los coeficientes LP y ceptrales, en los cuales podíamos más o menos distinguir algun tipo de correlación entre los coeficientes al distinguir un patron, son los que obtienen coeficientes de correlación Pearson más alejados del 0. En cambio los coefientes mel-cepstrum que tenían una representación más en forma de nube, son los que obtienen un coeficiente Pearson más cercano a 0. Estos valores y representaciones tienen sentido ya que un valor cercano a +1 o -1 implica una alta correlación entre componentes (podemos estimar el valor de uno en función del otro). En cambio un valor cercano a 0 indica que las componentes estan poco correladas y que la información conjunta proporcionada por ambas es el doble que la que otorga una sola de ellas.
  >
- Según la teoría, ¿qué parámetros considera adecuados para el cálculo de los coeficientes LPCC y MFCC?
> Para los LPCC se recomienda usar un orden de 13 coeficientes.
>
> Para los MFCC se recomienda usar:

> - Entre 24 y 40 filtros del banco mel.

> - Unos 13 coeficientes Mel-Ceptrales. A partir de 20 coeficientes, la información otorgada por los coeficientes podría confundir al sistema de reconocimiento de voz.

### Entrenamiento y visualización de los GMM.

Complete el código necesario para entrenar modelos GMM.

- Inserte una gráfica que muestre la función de densidad de probabilidad modelada por el GMM de un locutor
  para sus dos primeros coeficientes de MFCC.
  
- Inserte una gráfica que permita comparar los modelos y poblaciones de dos locutores distintos (la gŕafica
  de la página 20 del enunciado puede servirle de referencia del resultado deseado). Analice la capacidad
  del modelado GMM para diferenciar las señales de uno y otro.

### Reconocimiento del locutor.

Complete el código necesario para realizar reconociminto del locutor y optimice sus parámetros.

- Inserte una tabla con la tasa de error obtenida en el reconocimiento de los locutores de la base de datos
  SPEECON usando su mejor sistema de reconocimiento para los parámetros LP, LPCC y MFCC.
  
  >Adjuntamos a continuación los resultados obtenidos haciendo uso de los parámetros que mejor nos han funcionado para la parametrización MFCC.

  >Hemos usado 8 coeficientes de predicción lineal

  >Hemos usado 13 coeficientes cepstrales

  >Hemos usado _ coeficientes Mel-Cepstrales y _ filtros del banco de filtros.
  
  |                        | LP            | LPCC         | MFCC          |
  |------------------------|:-------------:|:------------:|:-------------:|
  | TASA DE ERROR          |   9.81% (77 errores)  |   3.06% (24 errores)   |   X.XX% (Y errores)   |
  
  >Estos resultados se han obtenido gracias a la elección de los siguientes parámetros para el gmm_train:

  > - Inicialización: VQ
  > - Número de gaussianas: 
  > - Threshold:  
  > - Número iteraciones: _ Este número en nuestro caso realmente no es muy relevante más que no entorpezca el threshold establecido ya que ajustamos el entrenamiendo de los modelos a través de este.
  ```c
  
  ```

### Verificación del locutor.

Complete el código necesario para realizar verificación del locutor y optimice sus parámetros.

- Inserte una tabla con el *score* obtenido con su mejor sistema de verificación del locutor en la tarea
  de verificación de SPEECON. La tabla debe incluir el umbral óptimo, el número de falsas alarmas y de
  pérdidas, y el score obtenido usando la parametrización que mejor resultado le hubiera dado en la tarea
  de reconocimiento.
  
  >Tal y como hemos visto en el apartado anterior, los resultados con MFCC son de largo los mejores para la tarea de reconocimiento de voz. La verificación obtenida es la siguiente:
 
  |                        | UMBRAL ÓPTIMO | FALSAS ALARMAS | PÉRDIDAS    | SCORE         |
  |------------------------|:-------------:|:------------:|:-------------:|:-------------:|
  | Verificación con MFCC  |   0   |   0   |   0   |   0   |
  
  >Para obtener estos resultados, sin tocar los modelos de usuarios ya entrenados, pasamos a entrenar el modelo del mundo. Procedemos de esta manera ya que la probabilidad de la GMM del usuario es muy variable igual que la del impostor. Por lo que normalizamos esta probabilidad respecto la de un modelo general como el citado anteriormente.
  
  >Los parámetros de entrenamiento de este modelo son:

  > - Inicialización: VQ
  > - Número de gaussianas: 
  > - Threshold:  
  > - Número iteraciones: _ 
  ```c
  
  ```
 
### Test final

- Adjunte, en el repositorio de la práctica, los ficheros `class_test.log` y `verif_test.log` 
  correspondientes a la evaluación *ciega* final.

>Tanto para la clasificación como para la verificación final, emplearemos los parámetros que nos han permitido conseguir una mejor puntuación en la base de datos SPEECON. Aunque el número de gaussianas tanto en el train como en el trainworld resulten muy especificos, hemos optimizado el umbral de criterio de parada del algoritmo de Expectation Maximization para evitar en la medida de lo posible un "overtraining" o "overfitting" que haga más difícil aun extrapolar estos parámetros a otras bases de datos u reconocimiento de señales distintas y por lo tanto tener unos modelos más generalizables. 

>Tambien es posible que si ajustamos el número de iteraciones de la inicialización o el threshold de mejora de la misma, podamos obtener un sistema de reconocimiento y de verificación más generalizables y que en algunas ocasiones, funcionen mejor.

### Trabajo de ampliación.

- Recuerde enviar a Atenea un fichero en formato zip o tgz con la memoria (en formato PDF) con el trabajo 
  realizado como ampliación, así como los ficheros `class_ampl.log` y/o `verif_ampl.log`, obtenidos como 
  resultado del mismo.
