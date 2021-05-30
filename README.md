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
  
  **sox** nos genera la señal en formato *raw*.
  
  **$X2X** nos permite la conversión entre distintos formatos de datos. En nuestro caso, la convierte a float (+sf).
  
  **$FRAME** extrae la trama de una secuencia de datos. En nuestro caso, con -l (240) indicamos la longitud y con -p (80) el periodo.
  
  **$WINDOW** le indicamos el tamaño de la ventana en su input (con -l, 240) y en su output (con -L, 240).
  
  **$LPC** nos calcula los coeficientes de la predicción lineal. Le indicamos la longitud de trama, con l- (240), el orden de LPC, con -m (con la variable $lpc_order), y el fichero output.

- Explique el procedimiento seguido para obtener un fichero de formato *fmatrix* a partir de los ficheros de
  salida de SPTK (líneas 45 a 47 del script `wav2lp.sh`).
  
  Para *fmatrix* necesitamos el número de filas y columnas ($nrow y $ncol). 
  
  *$ncol* tiene que ser igual al número de coeficientes, por lo que la obtenemos simplemente de sumarle 1 al orden del lpc ($lpc_order+1).
  
  Para *$nrow* (el número de tramas) convertimos la data de *$base.lp* con $X2X (con *+fa*, de float a ASCII, es decir, texto), y con *wc -l* contamos el número de líneas. 

  * ¿Por qué es conveniente usar este formato (u otro parecido)? Tenga en cuenta cuál es el formato de
    entrada y cuál es el de resultado.
    
    *fmatrix* nos permite pasarle un fichero de datos (en nuestro caso *base.lp*) y nos lo "ordena" como float en *nrow* filas y *ncol* columnas. De esta forma, podemos ver los datos de forma sencilla, concretamente, con *fmatrix_show*.

- Escriba el *pipeline* principal usado para calcular los coeficientes cepstrales de predicción lineal
  (LPCC) en su fichero <code>scripts/wav2lpcc.sh</code>:
  
  Usando el *'wav2lp.sh'* como plantilla, solo tenemos que cambiar los inputs de entrada, y las variables asignadas en el *sox*:
  
![image](https://user-images.githubusercontent.com/80445439/120103766-8d2d4c80-c151-11eb-99e6-657bf6ccd660.png)

![image](https://user-images.githubusercontent.com/80445439/120103775-99b1a500-c151-11eb-9a9b-b6f81c034202.png)

- Escriba el *pipeline* principal usado para calcular los coeficientes cepstrales en escala Mel (MFCC) en su
  fichero <code>scripts/wav2mfcc.sh</code>:

![image](https://user-images.githubusercontent.com/80445439/120103811-bcdc5480-c151-11eb-9ed4-be67cb77e45f.png)

![image](https://user-images.githubusercontent.com/80445439/120103821-c2d23580-c151-11eb-883b-c440f9ed0da0.png)

### Extracción de características.

- Inserte una imagen mostrando la dependencia entre los coeficientes 2 y 3 de las tres parametrizaciones
  para todas las señales de un locutor.
  
  + Indique **todas** las órdenes necesarias para obtener las gráficas a partir de las señales 
    parametrizadas.
  + ¿Cuál de ellas le parece que contiene más información?

- Usando el programa <code>pearson</code>, obtenga los coeficientes de correlación normalizada entre los
  parámetros 2 y 3 para un locutor, y rellene la tabla siguiente con los valores obtenidos.
  
  + Compare los resultados de <code>pearson</code> con los obtenidos gráficamente.

  ![image](https://user-images.githubusercontent.com/80445439/120117276-aa334100-c18c-11eb-92ac-7a242e80bd9e.png)

  Como podemos ver, hay mucha relación entre coeficientes en LP. En cambio para MFCC y LPCC hay menos correlación.
  
- Según la teoría, ¿qué parámetros considera adecuados para el cálculo de los coeficientes LPCC y MFCC?

### Entrenamiento y visualización de los GMM.

Complete el código necesario para entrenar modelos GMM.

- Inserte una gráfica que muestre la función de densidad de probabilidad modelada por el GMM de un locutor
  para sus dos primeros coeficientes de MFCC.
  
  Usando todos los coeficientes: 
  
  ![image](https://user-images.githubusercontent.com/80445439/120115345-92a38a80-c183-11eb-8e92-3bf5740132aa.png)

  Usando los dos primeros coeficientes:
  
  ![image](https://user-images.githubusercontent.com/80445439/120115390-b9fa5780-c183-11eb-8452-383207c26cbc.png)

  
- Inserte una gráfica que permita comparar los modelos y poblaciones de dos locutores distintos (la gŕafica
  de la página 20 del enunciado puede servirle de referencia del resultado deseado). Analice la capacidad
  del modelado GMM para diferenciar las señales de uno y otro.
  
  ![image](https://user-images.githubusercontent.com/80445439/120116085-b4ead780-c186-11eb-94e7-50181e23fac3.png)


### Reconocimiento del locutor.

Complete el código necesario para realizar reconociminto del locutor y optimice sus parámetros.

- Inserte una tabla con la tasa de error obtenida en el reconocimiento de los locutores de la base de datos
  SPEECON usando su mejor sistema de reconocimiento para los parámetros LP, LPCC y MFCC.
  
  ![image](https://user-images.githubusercontent.com/80445439/120115049-43a92580-c182-11eb-858a-85e6e27a1543.png)


### Verificación del locutor.

Complete el código necesario para realizar verificación del locutor y optimice sus parámetros.

- Inserte una tabla con el *score* obtenido con su mejor sistema de verificación del locutor en la tarea
  de verificación de SPEECON. La tabla debe incluir el umbral óptimo, el número de falsas alarmas y de
  pérdidas, y el score obtenido usando la parametrización que mejor resultado le hubiera dado en la tarea
  de reconocimiento.
 
 Con MFCC:
 
![image](https://user-images.githubusercontent.com/80445439/120115607-b3201480-c184-11eb-8aab-5eaf894e56fe.png)

 
### Test final

- Adjunte, en el repositorio de la práctica, los ficheros `class_test.log` y `verif_test.log` 
  correspondientes a la evaluación *ciega* final.

### Trabajo de ampliación.

- Recuerde enviar a Atenea un fichero en formato zip o tgz con la memoria (en formato PDF) con el trabajo 
  realizado como ampliación, así como los ficheros `class_ampl.log` y/o `verif_ampl.log`, obtenidos como 
  resultado del mismo.
