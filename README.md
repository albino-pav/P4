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
  - *SOX* : Serveix per canviar el format de la senyal d'entrada a un senyal adequat als nostres requeriments. Té els següents comandaments: 
    - -t raw : Ens indica que el format de sortida és .raw
    - -e signed: Ens indica quina codifiació de sortida tenim. En el nostre cas la tenim guardada com a integers amb símbol 
    - -b 16: Ens indica el número de bits que tenim a cada mostra codificada. En el nostre cas tenim codificacions de 16 bits.
  - *$X2X* : Serveix per convertir el format de dades d'entrada en un format estàndard de sortida, en aquest cas ho converteix a un short float. 
  - *$FRAME* : Serveix per extreure una frama d'una seqüència de dades i la converteix en una sèrie de frames amb possiblitat de superposició amb un cert període. 
    - -l 240: Indica que la llargada de la frama que extraiem és de 240 bits. 
    - -p 80: Indica que el període de superposició és de 80 bits.
  - *$WINDOW* : Multiplica element per element la llargada dels vectors d'entrada per una funció d'enfinestrat prèviament especificada. 
    - -l 240: Indica que la llargada de l'entrada és de 240 bits. 
    - -L 240: Indica que la llargada de la sortida és de 240 bits. 
  - *$LPC* : Calcula els coeficients de predicció lineal de dades enfinestrades amb una llargada L que entren per l'input donant com a output el seu resultat: 
    - -l 240: Indica que la llargada de la frama és de 240 bits. 
    - -m $lpc_order: Ens indica l'ordre de la predicció lineal. En aquest cas el que hem fet és agafar-lo amb un valor que podem anar canviant dins del programa. 
    - $base.lp : És el nom del fitxer de sortida.

- Explique el procedimiento seguido para obtener un fichero de formato *fmatrix* a partir de los ficheros de
  salida de SPTK (líneas 45 a 47 del script `wav2lp.sh`).
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.sh
 ncol=$((lpc_order+1)) # lpc p =>  (gain a1 a2 ... ap) 
 nrow=`$X2X +fa < $base.lp | wc -l | perl -ne 'print $_/'$ncol', "\n";'`
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 Observem com el número de columnes es l'ordre de lpc + 1. La primera ens indica el guany i les altres ens indiquen, si n'hem utilitzat, els coeficients utilitzats. 
 El número de files es tants com trames generades ($X2X), que guardem en format ASCII (+fa), a l'arxiu $base.lp El wc -l ens serveix per calcular el nombre de files. 

  * ¿Por qué es conveniente usar este formato (u otro parecido)? Tenga en cuenta cuál es el formato de
    entrada y cuál es el de resultado.  
    Ens interessa utilitzar aquest format ja que les columnes ens permet separar per coeficients i les files per trames ens permet veure clarament si hi ha algun error gran en un coeficient en concret, o si hi ha algun tros de la senyal que sigui molt diferent dels altres. Ho guardem en format ASCII que facilita la seva obertura en qualsevol ordinador.

- Escriba el *pipeline* principal usado para calcular los coeficientes cepstrales de predicción lineal
  (LPCC) en su fichero <code>scripts/wav2lpcc.sh</code>:  
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.sh
  sox $inputfile -t raw -e signed -b 16 - | $X2X +sf | $FRAME -l 180 -p 100 | $WINDOW -l 180 -L 180 |
	$LPC -l 180 -m $lpc_order | $LPC2C -m $lpc_order -M $lpcc_order > $base.lpcc
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Escriba el *pipeline* principal usado para calcular los coeficientes cepstrales en escala Mel (MFCC) en su
  fichero <code>scripts/wav2mfcc.sh</code>:
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.sh
  sox $inputfile -t raw -e signed -b 16 - | $X2X +sf | $FRAME -l 184 -p 106 | $WINDOW -l 240 -L 240 |
	$MFCC -l 240 -m $mfcc_order -s 8 -w 1 -n $bank_size > $base.mfcc 
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

### Extracción de características.

- Inserte una imagen mostrando la dependencia entre los coeficientes 2 y 3 de las tres parametrizaciones
  para todas las señales de un locutor.
  
  + Indique **todas** las órdenes necesarias para obtener las gráficas a partir de las señales 
    parametrizadas.
    Per extreure les senyals primer les hem tret com a .txt (ara estan mogudes a la carpeta grafics) i després hem creat un petit programa de python que ens les ha mostrat per pantalla. 

    Per extreure les senyals el que hem fet ha estat:
    1. LP:   fmatrix_show work/lp/BLOCK16/SES160/*.lp | egrep '^\['  | cut -f4,5 > lp_2_3.txt
    2. LPCC: fmatrix_show work/lp/BLOCK16/SES160/*.lpcc | egrep '^\[' | cut -f3,4 > lpcc_2_3.txt
    3. MFCC: fmatrix_show work/lp/BLOCK16/SES1600/*.mfcc | egrep '^\[' | cut -f3,4 > mfcc_2_3.txt

    Les senyals són:  
    1. LP
    <img src='https://github.com/sergiizquierdobas/P4/blob/flotats-izquierdo/grafics/lpgrafic.png'>  
  
    2. LPCC
    <img src='https://github.com/sergiizquierdobas/P4/blob/flotats-izquierdo/grafics/lpccgrafic.png'>
 
    3. MFCC  
    <img src='https://github.com/sergiizquierdobas/P4/blob/flotats-izquierdo/grafics/mfccgrafic.png'> 

      *Nota: Les imatges no són les que diem a la pipeline de dalt, ja que hem fet el readme   un altre dia i no recordem quina sessió vam agafar com a exemple*  
      
  + ¿Cuál de ellas le parece que contiene más información?  
  La que sembla que contingui més informació en el nostre cas és el gràfic de MFCC ja que (com comprovarem a la taula de sota) és el que gràfic que té els coeficients més incorrelats.

- Usando el programa <code>pearson</code>, obtenga los coeficientes de correlación normalizada entre los
  parámetros 2 y 3 para un locutor, y rellene la tabla siguiente con los valores obtenidos.

  |                        | LP   | LPCC | MFCC |
  |------------------------|:----:|:----:|:----:|
  | &rho;<sub>x</sub>[2,3] |-0,442|0,3825|0,2169|
  
  + Compare los resultados de <code>pearson</code> con los obtenidos gráficamente.  

  Podem veure com els valors de lp a lpcc respectivament es van dispersant, i per tant el seu valor de la correlació normalitzada entre els paràmetres 2 i 3 disminueix. 
  
- Según la teoría, ¿qué parámetros considera adecuados para el cálculo de los coeficientes LPCC y MFCC?  

Per al LPCC, el Linear Prediction Cepstral Coeficients, ens diu que hem d'utilitzar una prediccio P d'ordre 12 i per la longitud de les trames de entre 20-30ms i entre 10-15ms.  
Per altra banda, pel MFCC, els Mel Frequency Cepstral Coeficients, es solen utilitzar els primers 13 coeficients per a la tasca de reconeixement de veu i es recomana utilitzar un banc de 24-26 filtres. Per la resta de parametres, són els mateixos que per LPCC.

### Entrenamiento y visualización de los GMM.

Complete el código necesario para entrenar modelos GMM.

- Inserte una gráfica que muestre la función de densidad de probabilidad modelada por el GMM de un locutor
  para sus dos primeros coeficientes de MFCC.
<img src = 'https://github.com/sergiizquierdobas/P4/blob/flotats-izquierdo/grafics/DensidadProbabilidadLocutor.png'>

- Inserte una gráfica que permita comparar los modelos y poblaciones de dos locutores distintos (la gŕafica
  de la página 20 del enunciado puede servirle de referencia del resultado deseado). Analice la capacidad
  del modelado GMM para diferenciar las señales de uno y otro.
  * En el caso de tener el modelo de GMM del locutor 10 y población del locutor 10.  
  <img src = 'https://github.com/sergiizquierdobas/P4/blob/flotats-izquierdo/grafics/Densitatprobabilitat1010.png'>
  * En el caso de tener el modelo de GMM del locutor 11 y población del locutor 10.  
  <img src = 'https://github.com/sergiizquierdobas/P4/blob/flotats-izquierdo/grafics/DensidadProbabilidad1110.png'>
  * En el caso de tener el modelo de GMM del locutor 10 y población del locutor 11.
  <img src = 'https://github.com/sergiizquierdobas/P4/blob/flotats-izquierdo/grafics/DensidadProbabilidad1011.png'>
  * En el caso de tener el modelo de GMM del locutor 11 y población del locutor 11.
  <img src = 'https://github.com/sergiizquierdobas/P4/blob/flotats-izquierdo/grafics/DensidadProbabilidad1111.png'>

### Reconocimiento del locutor.

Complete el código necesario para realizar reconociminto del locutor y optimice sus parámetros.

- Inserte una tabla con la tasa de error obtenida en el reconocimiento de los locutores de la base de datos
  SPEECON usando su mejor sistema de reconocimiento para los parámetros LP, LPCC y MFCC.
  |                        | LP   | LPCC | MFCC |
  |------------------------|:----:|:----:|:----:|
  | Tasa de error (%)      | 8,54 | 1,78 | 2,17 |

### Verificación del locutor.

Complete el código necesario para realizar verificación del locutor y optimice sus parámetros.

- Inserte una tabla con el *score* obtenido con su mejor sistema de verificación del locutor en la tarea
  de verificación de SPEECON. La tabla debe incluir el umbral óptimo, el número de falsas alarmas y de
  pérdidas, y el score obtenido usando la parametrización que mejor resultado le hubiera dado en la tarea
  de reconocimiento.

  1. LP  
  <img src='https://github.com/sergiizquierdobas/P4/blob/flotats-izquierdo/captures/verif_err_lp.png'>

  2. LPCC  
  <img src='https://github.com/sergiizquierdobas/P4/blob/flotats-izquierdo/captures/verif_err_lpcc.png'>
 
  3.  MFCC  
  <img src='https://github.com/sergiizquierdobas/P4/blob/flotats-izquierdo/captures/verif_err_mfcc.png'> 

  Tot i que durant el reconeixement el millor resultat l'obtenim a través de fer servir paràmetres LPCC, quan passem a la segona verificació el millor resultat és clarament a través de MFCC. No obstant la diferència en el reconeixement és molt petita (de un 0,39%). Per tant per a la última verificació farem servir els següents valors:

  La taula amb els valors obtinguts amb MFCC és: 
  |         | Llindar  | Falsa alarma | Pèrdua | Score |
  |---------|:--------:|:------------:|:------:|:-----:|
  | MFCC    | 0,284349 |    0/1000    | 68/250 |  27.2 |

### Test final

- Adjunte, en el repositorio de la práctica, los ficheros `class_test.log` y `verif_test.log` 
  correspondientes a la evaluación *ciega* final.

### Trabajo de ampliación.

- Recuerde enviar a Atenea un fichero en formato zip o tgz con la memoria (en formato PDF) con el trabajo 
  realizado como ampliación, así como los ficheros `class_ampl.log` y/o `verif_ampl.log`, obtenidos como 
  resultado del mismo.
