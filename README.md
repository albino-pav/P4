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
  ```sh
  sox $inputfile -t raw -e signed -b 16 - | $X2X +sf | $FRAME -l 240 -p 80 | $WINDOW -l 240 -L 240 |
  $LPC -l 240 -m $lpc_order > $base.lp
  ```

  `sox`: Este programa, que ya utilizamos en la primera práctica, nos ayuda a convertir una señal en formato wave a formato raw (-t) de 16 bits (-b) con signo (-e), para que posteriormente `X2X` pueda tratar el fichero, ya que solo puede leer en formato raw.

  `$X2X`: Este es un programa de `SPTK` que nos permite convertir el fichero que inicialmente era de valores short a valores float, es decir, reales en coma flotante de 32 bits (+sf).

  `$FRAME`: También se trata de un programa de `SPTK`  que divide la señal de entrada en tramas de 240 muestras (-l) con un desplazamiento de ventana de 80 muestras (-p).

  `$WINDOW`:  Este también es un programa de `SPTK`que aplica una ventana (por defecto se usa la ventana de Blackman) a la señal de 240 muestras (-l) y la convierte en una señal con frames de 240 muestras (-L).

  `$LPC`:  También se trata de un programa de `SPTK` que calcula los primeros coeficientes (-m) de la ganancia de la predicción lineal en tramas de 240 muestras (-l).

  El resultado de esta parametrización se guarda en el fichero `$base.lp`, es decir, tendrá el mismo nombre que el archivo de entrada.


- Explique el procedimiento seguido para obtener un fichero de formato *fmatrix* a partir de los ficheros de
  salida de SPTK (líneas 45 a 47 del script `wav2lp.sh`).
  ```sh
  # Our array files need a header with the number of cols and rows:
  ncol=$((lpc_order+1)) # lpc p =>  (gain a1 a2 ... ap) 
  nrow=`$X2X +fa < $base.lp | wc -l | perl -ne 'print $_/'$ncol', "\n";'`

  # Build fmatrix file by placing nrow and ncol in front, and the data after them
  echo $nrow $ncol | $X2X +aI > $outputfile
  cat $base.lp >> $outputfile
  ```

  El fichero fmatrix está formado por el número de filas (nrow) y el número de columnas (ncol) seguido de los datos. 

  El número de columnas corresponde al orden del predictor lpc+1, que es el número de coeficientes del mismo. En cambio, el número de filas corresponde al número de tramas del archivo parametrizado. Para esto, utilizando nuevamente el programa `X2X` convertimos la señal en texto (+fa) y contamos el número de lineas utilizando el comando de `UNIX` wc (-l). Finalmente construimos el fichero de salida convirtiendo los valores del número de filas y columnas a enteros sin signo de 4 bytes (+ai) usando `X2X`.

  * ¿Por qué es conveniente usar este formato (u otro parecido)? Tenga en cuenta cuál es el formato de
    entrada y cuál es el de resultado.

    Inicialmente, teníamos una señal de voz modificada con ley mu de 8 bits. Esto no es muy conveniente debido al orden de los coeficientes. Por lo que el resultado que obtenemos, el valor de los coeficientes en cada trama de forma matricial, facilitará la lectura de estos.

- Escriba el *pipeline* principal usado para calcular los coeficientes cepstrales de predicción lineal
  (LPCC) en su fichero <code>scripts/wav2lpcc.sh</code>:

  ```sh
  sox $inputfile -t raw -e signed -b 16 - | $X2X +sf | $FRAME -l 240 -p 80 |
  $WINDOW -l 240 -L 240 | $LPC -l 240 -m $lpc_order | 
  $LPC2C -m $lpc_order -M $cepstrum_order > $base.cep
  ```

- Escriba el *pipeline* principal usado para calcular los coeficientes cepstrales en escala Mel (MFCC) en su
  fichero <code>scripts/wav2mfcc.sh</code>:

  ```sh
  sox $inputfile -t raw -e signed -b 16 - | $X2X +sf | $FRAME -l 240 -p 80 | 
  $WINDOW -l 240 -L 240 |
  $MFCC -l 240 -m $mfcc_order -n $number_filters > $base.mfcc
  ```

### Extracción de características.

- Inserte una imagen mostrando la dependencia entre los coeficientes 2 y 3 de las tres parametrizaciones
  para todas las señales de un locutor.

    <img src="/img/img1.png" width="1200" align="center">

  + Indique **todas** las órdenes necesarias para obtener las gráficas a partir de las señales 
    parametrizadas.

    Para obterner los ficheros de texto hemos usado los siguientes comandos en el terminal:

    ```console
    fmatrix_show work/lp/BLOCK01/SES017/*.lp | egrep '^\[' | cut -f4,5 > lp_2_3.txt
    fmatrix_show work/lpcc/BLOCK01/SES017/*.lpcc | egrep '^\[' | cut -f3,4 > lpcc_2_3.txt
    fmatrix_show work/mfcc/BLOCK01/SES017/*.mfcc | egrep '^\[' | cut -f3,4 > mfcc_2_3.txt
    ```

    Seguidamente para mostrar los resultados, hemos ejecutado el siguiente código en python:

    ```py
    import matplotlib.pyplot as plt
    import matplotlib.cbook as cbook
    import numpy as np

    lp = np.loadtxt('lp_2_3.txt')
    lpcc = np.loadtxt('lpcc_2_3.txt')
    mfcc = np.loadtxt('mfcc_2_3.txt')

    fig, (axlp,axlpcc,axmfcc) = plt.subplots(3)
    fig.suptitle("Coeficientes 2 y 3 usando LP, LPCC y MFCC de las senales de un locutor")
    axlp.plot(lp[:, 0], lp[:, 1],'.')
    axlpcc.plot(lpcc[:, 0], lpcc[:, 1],'.')
    axmfcc.plot(mfcc[:, 0], mfcc[:, 1],'.')
    axlp.set_title('LP')
    axlp.set(xlabel='Coeficiente 2', ylabel='Coeficiente 3')
    axlpcc.set_title('LPCC')
    axlpcc.set(xlabel='Coeficiente 2', ylabel='Coeficiente 3')
    axmfcc.set_title('MFCC')
    axmfcc.set(xlabel='Coeficiente 2', ylabel='Coeficiente 3')
    axlp.grid()
    axlpcc.grid()
    axmfcc.grid()
    plt.show()
    ```

    Finalmente para ejecutar el código anterior usamos la siguiente orden en el terminal:

    ```console
    python ex2.py &
    ```

    Cabe destacar que no detecta la "ñ" como un carácter en ASCII y por eso hemos tenido que sustituirla. También hemos modificado los parámetros de la gráfica para que los títulos no se superpusieran con los ejes de la gràfica superior.

  + ¿Cuál de ellas le parece que contiene más información?

    Entendemos esta pregunta como ver la cantidad de coeficientes correlados que hay entre ellos. Si la gráfica que obtenemos es una linea recta, significa que hay poca información entre los coeficientes, ya que a partir de uno podremos calcular el otro. En cambio, dependiendo del tipo de parametrización, observamos:

    Para la parametricación LP, la información entre los coeficientes tiende a tener una forma lineal cada vez más estrecha, por tanto no aporta mucha información.

    En el caso de la parametrización LPCC se observa en la gráfica que los coeficientes muestran una mayor dispersión, sobretodo para valores bajos del segundo coeficiente por tanto la información con esta parametrización es mayor.

    Por último, usando la parametrización MFCC observamos que en esta gráfica la información está más dispersa respecto al caso anterior, lo vemos en que el márgen dinámico de ambos coeficientes es mucho más elevado.

    En definitiva, la parámetrización que contiene más información es la MFCC ya que sus coeficientes estan más incorrelados ente ellos, por lo que será más complicado predecir el siguiente.

- Usando el programa <code>pearson</code>, obtenga los coeficientes de correlación normalizada entre los
  parámetros 2 y 3 para un locutor, y rellene la tabla siguiente con los valores obtenidos.

  Con las siguientes instrucciones en el terminal:

  ```console
  pearson work/lp/BLOCK01/SES017/*.lp
  pearson work/lpcc/BLOCK01/SES017/*.lpcc
  pearson work/mfcc/BLOCK01/SES017/*.mfcc
  ```

  |                        | LP   | LPCC | MFCC |
  |------------------------|:----:|:----:|:----:|
  | &rho;<sub>x</sub>[2,3] | -0.873263     |0.160985      |0.316451      |
  
  + Compare los resultados de <code>pearson</code> con los obtenidos gráficamente.
    
    Si el valor del módulo de rho_x se aproxima a 1 significa que la correlación entre los coeficientes es alta. En cambio, si se aproxima a 0, significa que la correlación es baja.

    Para el caso de la parametrización LP observamos que el módulo de rho_x  se aproxima a 1, por lo que la correlación es muy correlada y aporta poca información. Esto coincide con la gráfica del apartado anterior, donde hemos llegado a la misma conclusión.

    Para las parametrizaciones LPCC y MFCC vemos que el módulo de rho_x se aproxima a 0 por lo que los coeficientes 2 y 3 son bastante incorrelados y por tanto contienen más información. Esto, también coincide con las gráficas.

    No obstante, vemos que los coeficientes del LPCC són significativamente más incorrelados que los del MFCC así que aportan más información. Esto no coincide con las gràficas del apartado anterior.
  
- Según la teoría, ¿qué parámetros considera adecuados para el cálculo de los coeficientes LPCC y MFCC?

  Para la parametrización de LPCC la teoría indica que los coeficientes cepstrales tienen que tener como valor 3/2 por el orden del predictor LPCC. Nosotros hemos escogido orden 24 y 36 coeficientes cepstrales.

  En el caso de la parametrización MFCC la teoría indica que el orden toma valor 13 y el numero de filtros deberia estar entre 24 y 40. Nosotros hemos utilizado 18 coeficientes y 40 filtros.

### Entrenamiento y visualización de los GMM.

Complete el código necesario para entrenar modelos GMM.

- Inserte una gráfica que muestre la función de densidad de probabilidad modelada por el GMM de un locutor
  para sus dos primeros coeficientes de MFCC.

  Para obtener la gráfica del locutor 17 hemos puesto en el terminal el siguiente comando:

  ```console
  plot_gmm_feat work/gmm/mfcc/SES017.gmm work/mfcc/BLOCK01/SES017/*.mfcc &
  ```
  
  <img src="/img/img2.png" width="1200" align="center">

  Para obtener la gráfica del locutor 43 hemos puesto en el terminal el siguiente comando:

  ```console
  plot_gmm_feat work/gmm/mfcc/SES043.gmm work/mfcc/BLOCK04/SES043/*.mfcc &
  ```

  <img src="/img/img3.png" width="1200" align="center">
  
- Inserte una gráfica que permita comparar los modelos y poblaciones de dos locutores distintos (la gŕafica
  de la página 20 del enunciado puede servirle de referencia del resultado deseado). Analice la capacidad
  del modelado GMM para diferenciar las señales de uno y otro.

  Para el locutor 17 con su correspondiente población ejecutamos el comando:

  ```console
  plot_gmm_feat work/gmm/mfcc/SES017.gmm work/mfcc/BLOCK01/SES017/*.mfcc -f blue -g red &
  ```

  <img src="/img/img4.png" width="1200" align="center">

  Para el locutor 43 con su correspondiente población ejecutamos el comando:

  ```console
  plot_gmm_feat work/gmm/mfcc/SES043.gmm work/mfcc/BLOCK04/SES043/*.mfcc -f blue -g red &
  ```

  <img src="/img/img5.png" width="1200" align="center">

  Para el locutor 17 (rojo) con la población del locutor 43 (azul) usamos el comando:

  ```console
  plot_gmm_feat work/gmm/mfcc/SES017.gmm work/mfcc/BLOCK04/SES043/*.mfcc -f blue -g red &
  ```

  <img src="/img/img6.png" width="1200" align="center">

  Para el locutor 43 (rojo) con la población del locutor 17 (azul) usamos el comando:

  ```console
  plot_gmm_feat work/gmm/mfcc/SES043.gmm work/mfcc/BLOCK01/SES017/*.mfcc -f blue -g red &
  ```

  <img src="/img/img7.png" width="1200" align="center">

  Observamos que en los casos de que la población coincide con el locutor las zonas azules estan dentro de la regiones con el 50% de densidad, por lo que estan repartidas de manera correcta. En los casos en que la población no coincide con su locutor, la densidad de población no se corresponde con las regiones marcadas.
  
  Este resultdo es el esperado ya que nos ayudará a diferenciar si un candidato es un impostor o es legítimo.

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
