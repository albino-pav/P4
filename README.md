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
  >***sox***: Sirve para cambiar el formato de una señal de entrada a uno de salida que nos convenga. Para saber las características de sox, escribimos sox -h en el terminal. En nuestro caso, al utilizar *-t raw* estamos diciendo que queremos un fichero tipo raw. Con *-e signed* definimos una codificación signed integer. Por último, *-b 16* nos dice que queremos 16 bits.
 
  >***X2X***: Programa de sptk que sirve para transformar datos input a otro formato output. La manera de utilizar este comando en el terminal es la siguiente: **x2x [+type1 [+type2][–r] [–o] [%format]**. En nuestro caso, *+sf* transforma los datos a short int format. 
  
  >***FRAME***: Extrae el frame de la secuencia de datos. *-l* indica la longitud del frame, y *-p* indica el periodo del frame.
  
  >***WINDOW***: Enventanado de ventana. *-l* indica la longitud de frames del input. *-L* indica la longitud de frames del output.
  
  >***LPC***: Calcula los coeficientes de predicción lineal. *-l* indica la longitud de frames, y *-m* indica el orden de coeficientes LPC. 

- Explique el procedimiento seguido para obtener un fichero de formato *fmatrix* a partir de los ficheros de
  salida de SPTK (líneas 45 a 47 del script `wav2lp.sh`).
  
  >El número de columnas del fichero es el orden de los coeficientes LPC + 1, hacemos esto porque el primer coeficiente contiene la información de la ganancia. El número de filas es el número de frames de la señal, y guardaremos los datos en ascii, ya que hacemos *+fa* (de float a ascii). 

  * ¿Por qué es conveniente usar este formato (u otro parecido)? Tenga en cuenta cuál es el formato de
    entrada y cuál es el de resultado.
  > Es conveniente usar este formato porque así es más fácil acceder a los datos porque estan diferenciadoa para cada frame. Luego los podremos utilizar en otros programas o mostrarlos gráficamente.

- Escriba el *pipeline* principal usado para calcular los coeficientes cepstrales de predicción lineal
  (LPCC) en su fichero <code>scripts/wav2lpcc.sh</code>:
  > sox $inputfile -t raw -e signed -b 16 - | $X2X +sf | $FRAME -l 240 -p 80 | $WINDOW -l 240 -L 240 |
	  $LPC -l 240 -m $lpc_order | $LPC2C -m $lpc_order -M $nceps > $base.lpcc

- Escriba el *pipeline* principal usado para calcular los coeficientes cepstrales en escala Mel (MFCC) en su
  fichero <code>scripts/wav2mfcc.sh</code>:
  > sox $inputfile -t raw -e signed -b 16 - | $X2X +sf | $FRAME -l 240 -p 80 |	
   $MFCC -s 8000 -n $nfiltros -l 240 -m $mfcc_order > $base.mfcc

### Extracción de características.

- Inserte una imagen mostrando la dependencia entre los coeficientes 2 y 3 de las tres parametrizaciones
  para todas las señales de un locutor.
  
  + Indique **todas** las órdenes necesarias para obtener las gráficas a partir de las señales 
    parametrizadas.
    >LP
    ><img width="765" alt="comando lp" src="https://user-images.githubusercontent.com/79308448/118698554-d6f06b80-b810-11eb-9a89-f804c1655e24.PNG">

<img width="958" alt="lp grafica" src="https://user-images.githubusercontent.com/79308448/118700688-3a7b9880-b813-11eb-8d15-0cad3cf62bc4.PNG">

    >LPCC
    ><img width="795" alt="lpcc comando" src="https://user-images.githubusercontent.com/79308448/118698578-dce64c80-b810-11eb-8923-1cab5efd443a.PNG">

<img width="929" alt="lpcc grafica" src="https://user-images.githubusercontent.com/79308448/118700724-436c6a00-b813-11eb-858d-aeefcfcdd825.PNG">

    >MFCC
    ><img width="798" alt="comando mfcc" src="https://user-images.githubusercontent.com/79308448/118698591-e1ab0080-b810-11eb-9c33-cb11068cad41.PNG">

<img width="891" alt="mfcc grafica" src="https://user-images.githubusercontent.com/79308448/118700753-4a937800-b813-11eb-81ef-ac457fa16530.PNG">

  + ¿Cuál de ellas le parece que contiene más información?

- Usando el programa <code>pearson</code>, obtenga los coeficientes de correlación normalizada entre los
  parámetros 2 y 3 para un locutor, y rellene la tabla siguiente con los valores obtenidos.

  |                        | LP   | LPCC | MFCC |
  |------------------------|:----:|:----:|:----:|
  | &rho;<sub>x</sub>[2,3] |-0.562927|0.351929|-0.622987|
  
  + Compare los resultados de <code>pearson</code> con los obtenidos gráficamente.
  
- Según la teoría, ¿qué parámetros considera adecuados para el cálculo de los coeficientes LPCC y MFCC?

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

### Verificación del locutor.

Complete el código necesario para realizar verificación del locutor y optimice sus parámetros.

- Inserte una tabla con el *score* obtenido con su mejor sistema de verificación del locutor en la tarea
  de verificación de SPEECON. La tabla debe incluir el umbral óptimo, el número de falsas alarmas y de
  pérdidas, y el score obtenido usando la parametrización que mejor resultado le hubiera dado en la tarea
  de reconocimiento.
 
### Test final

- Adjunte, en el repositorio de la práctica, los ficheros `class_test.log` y `verif_test.log` 
  correspondientes a la evaluación *ciega* final.

### Trabajo de ampliación.

- Recuerde enviar a Atenea un fichero en formato zip o tgz con la memoria (en formato PDF) con el trabajo 
  realizado como ampliación, así como los ficheros `class_ampl.log` y/o `verif_ampl.log`, obtenidos como 
  resultado del mismo.
