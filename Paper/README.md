# Title
* 

# Estructura de paper

## Keywords
* Distributed Particle Swarm Optimization
* Convolutional Neural Networks (¿?)
* Aquifer hydraulic parameters
* Optimization (¿?)
* Simulation - Optimization model

## Introducción
Las aguas subterráneas juegan un rol muy importante en la Gestión Integrada de Recursos Hídricos (GIRH). Siendo aún más relevante en el balance hídrico en zonas donde el recurso superficial es escaso \citep{Liuetal2022}. Por esta razón, en la GIRH, cada vez se ha hecho más necesario el uso de herramientas de modelación que permitan simplificar, optimizar y entender los distintos procesos que ocurren en las cuencas y acuíferos. Estas labores pueden llegar a ser complicadas dependiendo de las características del acuífero de interés \citep{Sanzanaetal2019}. En este sentido, una adecuada modelación de los sistemas de aguas subterráneas depende de un buen conocimiento de los parámetros hidrogeológicos del acuífero, como la conductividad hidráulica, transmisividad, coeficiente de almacenamiento, rendimiento específico y la tasa de recarga del acuífero \citep{LakshmiPrasadAndRastogi2001}. Sin embargo, estos parámetros comunmente necesitan ser estimados ya que no son fáciles de medir directamente pues requieren considerables recursos humanos y económicos \citep{Batenietal2015}. 
    
En los últimos años, investigadores han adoptado el modelado inverso de aguas subterráneas como un enfoque matemático válido para estimar los parámetros de los acuíferos \citep{Carreraetal2005, HendricksFranssenetal2009, Mohairetal2017, Pateletal2022}. En este sentido, se utilizan Simulation optimization (SO) models, en donde los parámetros distribuidos se asignan a un modelo matemático con condiciones de contorno conocidas, cuyos resultados alimentan al modelo de optimización, el cual tiene el objetivo de asegurar la minimización de errores entre las variables observadas y simuladas para obtener valores óptimos de los parámetros hidráulicos \citep{LakshmiPrasadAndRastogi2001, Pateletal2022}. La simulación del sistema subterráneo se realiza utilizando modelos basado en cuadrículas o mallas, como los modelos de diferencias finitas (FDM) o de elementos finitos (FEM); o simuladores independientes de una malla, como Meshfree (Mfree). Mientras que, por otro lado, los modelos de optimización métodos tradicionales como nonlinear programming (NLP) techniques basadas en gradientes (*CITAS*), por ejemplo, the steepest descent method, conjugate gradient method, Gauss–Newton method, etc; y métodos no tradicionales, como los algoritmos evolutivos (*CITAS*), por ejemplo, (*****). La desventaja de los algorítmos basados en gradientes es que pueden dar como resultado valores óptimos locales en lugar de globales debido a la falta de convexidad inherente en los modelos de acuíferos, ya que la ecuación del modelo de flujo puede ser lineal con respecto a una variable de estado, que a su vez es altamente no lineal con respecto a los parámetros del sistema \citep{LakshmiPrasadAndRastogi2001, Batenietal2015}. Por tanto, para abordar estos inconvenientes (*shortcomings*) se aplican los algoritmos evolutivos, ya que pueden manejar problemas altamente no lineales y convergen al óptimo global en lugar del local \citep{Batenietal2015}. 

Hablar de otros papers con metodologías distribuidas








------







* Antecedentes a calibración de PH de un acuífero.

    Las aguas subterráneas juegan un rol muy importante en la Gestión Integrada de Recursos Hídricos (GIRH). Siendo aún más relevante en el balance hídrico de áreas donde la dinámica río-acuífero afecta las secciones del lecho del río, o donde las alcantarillas están ubicadas debajo del nivel del agua subterránea (Sanzana et al., 2019b), o en zonas donde el recurso superficial es escaso (Liu et al., 2022). Por esta razón, cada vez se ha hecho más necesario el uso de herramientas de modelación que permitan simplificar y/u optimizar distintos procesos. En la GIRH estas labores pueden llegar a ser complicadas dependiendo de las características del acuífero de interés (Sanzana et al., 2019a; b). En este sentido, una adecuada modelación de los sistemas de aguas subterráneas depende de un buen conocimiento de los parámetros hidrogeológicos del acuífero, como la conductividad hidráulica, transmisividad, coeficiente de almacenamiento, rendimiento específico y la tasa de recarga del acuífero (Lakshmi Prasad y Rastogi 2001). Sin embargo, estos parámetros comunmente necesitan ser estimados ya que no son fáciles de medir directamente pues requieren considerables recursos humanos y económicos (Bateni et al., 2015). 
    
    En los últimos años, investigadores han adoptado el modelado inverso de aguas subterráneas como un enfoque matemático válido para estimar los parámetros de los acuíferos (Carrera et al., 2005 *+CITAS*). En este sentido, se utilizan modelos de simulación optimización (Simulation optimization (SO) models), en donde los parámetros distribuidos se asignan a un modelo matemático con condiciones de contorno conocidas, cuyos resultados alimentan al modelo de optimización, el cual tiene el objetivo de asegurar la minimización de errores entre las variables observadas y simuladas para obtener valores óptimos de los parámetros hidráulicos (Lakshmi Prasad y Rastogi 2001; Patel et al., 2022). La simulación del sistema subterráneo se realiza utilizando modelos basado en cuadrículas o mallas, como los modelos de diferencias finitas (FDM) o de elementos finitos (FEM); o simuladores independientes de una malla, como Meshfree (Mfree). Mientras que, los algoritmos de optimización ampliamente usados son aquellos que usan técnicas de programación no lineal (nonlinear programming (NLP) techniques) (*CITAS*) como the steepest descent method, conjugate gradient method, Gauss–Newton method, etc. Sin embargo, las técnicas clásicas de optimización basadas en gradientes pueden dar como resultado valores óptimos locales en lugar de globales debido a la falta de convexidad inherente en los modelos de acuíferos, ya que la ecuación del modelo de flujo puede ser lineal con respecto a una variable de estado, que a su vez es altamente no lineal con respecto a los parámetros del sistema (Lakshmi Prasad y Rastogi 2001; Bateni et al., 2015). Por tanto, para abordar estos inconvenientes (*shortcomings*) se aplican métodos no tradicionales, como los algoritmos evolutivos, ya que pueden manejar problemas altamente no lineales y convergen al óptimo global en lugar del local (Bateni et al., 2015). 

    [Hablar de algorítmos evolutivos --> PSO]
    En el área de las aguas subterráneas, los algorítmos evolutivos han sido evaluados satisfactoriamente en diferentes usos, por ejemplo, GA ....

    Thomas et al., 2018
    [Hablar de convolución]

    En la presente investigación se plantea un modelo de simulación optimización (SO model), en donde el modelo de optimización utiliza la combinación de un algorítmo evolutivo, Particle Swarm Optimization (PSO) y las Convolutional Neural Networks para la estimación adecuada de los parámetros hidráulicos de un acuífero real. Mientras que la simulación del sistema subterráneo se realiza con un modelo de diferencias finitas (FDM), MODFLOW, el cuál está acoplado a un modelo de hidrología superficial, WEAP, los cuales permiten una mejor representación de los precesos de recarga y descarga del sistema. 

    [Metodología breve]

    Las variables de decisión son la conductividad hidráulica, rendimiento y almacenamiento específico

    [Vacío en el conocimiento a abordar]

    ---

    Hablar del modelo, considerando que es una desventaja el tiempo de modelación aunque se ha implementado una metodología de ejecución en paralelo que permite reducir los tiempos de simulación.

    Aplicaciones de PSO y Convolución en hidrología e hidrogeología.
    Una de las críticas a los algorítmos genéticos es que requieren muchas evaluaciones de funciones antes de llegar a la solución óptima superior (Lingireddy, 1997) y aunque los avances tecnológicos han hecho que esto no sea tan crítico, el problema persiste al evaluar acuíferos muy grandes (Lingireddy, 1997). [ ---- Aquí hablaría de la paralelización ---- ]

    Sin embargo, en la presente investigación se hará uso también de Convoluciones [ ---- Previamente poner antecedentes de las convoluciones en ciencias físicas ---- luego explicar porqué es conveniente usarlas juntas ---- ]

    Los algorítmos genéticos (GA) Lsolo se ocupan de problemas de optimización sin restricciones (Lingireddy, 1997). Los GA con un enfoque indirecto tienen la ventaja que es adecuado para situaciones en las que los datos disponibles son escasos (Lingireddy, 1997). DeJong(1975) recommended a high probability of crossover along with a low probability of mutation for good convergence characteristics of a genetic algorithm. Typical values of probabilities of crossover and mutation are 0.6 ~ 0.7 (0 - 1) and 0.02 ~ 0.03 (0 - 0.1) respectively (Lingireddy, 1997).


* Problema a resolver¨--> Objetivo y vació en el conocimiento.

    ### Objetivo principal
    * Estimar los parámetros hidráulicos de un acuífero utilizando modelación inversa con algorítmos bioinspirados y convolutional neural networks junto a un modelo integrado de recursos hídricos.
    ### Objetivo específco
    * Optimizar la calibración de un modelo subterráneo utilizando PSO (Particle Swarm Optimization) y Convolución
    * Calibrar paramétros hidráulicos (variables de decisión): 
        * Conductividad hidráulica (Kx y Kz) --> Considerando Ky = Kx
        * Rendimiento específico (Sy) --> Considerando que Almacenamiento específico (Ss) = Sy / 100
        * Supuesto: No hay variación de los parámentros en el tiempo. Limitación del programa.
    * Calcular la incertidumbre asociada a los valores de las variables de decisión.
    * Definir las funciones de pérdida.
    * Metodología aplicada a un acuífero real --> Ligua - Petorca, Chile central.

    . [Encontrar el set de parámetros óptimos que reduzca el error (qué monitorearemos - fitness function (¿?)) entre los valores observados y simulados] --> Se plantea un modelo de simulación - optimización (SO).
## Data and  Methodology

### Optimization models

#### Distributed Particle Swarm Optimization 
Para introducirnos al Distributed Particle Swarm Optimization algorithm (DPSO), debemos conocer como funciona el algorítmo PSO básico. PSO es un algoritmo evolutivo estocástico propuesto por Eberhart y Kennedy (1995) basado en la inteligencia colectiva de la población (conocido como enjambre). Una población consiste en partículas que se mueven a través del espacio de búsqueda multidimensional y cambian de posición, dependiendo de su propia experiencia (la mejor posición individual actual, pbest) y la experiencia de las otras partículas (la mejor posición global actual, gbest) (Erdeljan et al., 2014; Thomas et al., 2018). En cada generación, las partículas actualizan su posición cambiando su velocidad hacia pbest y gbest 

El cambio de posición de la partícula i se logra moviendo la partícula de la posición anterior, según la ecuación:


Kennedy y Eberhart [18], inspirados en el comportamiento de una bandada de pájaros en busca de comida [19], desarrollaron el algoritmo PSO que sigue las características de comportamiento comunes de los animales que se mueven en grupos. . Al principio, el algoritmo se desarrolló para sistemas continuos y, más tarde, se introdujeron algoritmos para sistemas discretos: PSO binario [20] y PSO entero [21-23]. Con el algoritmo binario cada partícula de la población puede tomar valores binarios (0 o 1). En casos más generales, como PSO entero, se logra un valor óptimo redondeando el óptimo real al entero más cercano.




El algoritmo PSO distribuido se basa en la búsqueda de soluciones disponibles en el espacio paralelo [25]. La población (enjambre) consiste en varios sub-enjambres distribuidos, asignados a diferentes procesadores

Independientemente de los subenjambres restantes, cada procesador ejecuta el algoritmo (un número definido de iteraciones) en los subenjambres locales. Después de un número de iteraciones previamente definido, se intercambian soluciones de diferentes sub-enjambres. La modificación en el algoritmo distribuido es la introducción de un nuevo período de sincronización de parámetros (Tsync), que define la frecuencia de comunicación entre sub-enjambres. El parámetro Tsync representa el número de iteraciones después de las cuales se actualizará el óptimo global (bg). Cuando los subenjambres reciben información sobre el óptimo global, cambian de velocidad como se muestra en las ecuaciones. 7-10.


#### Integrated Managment Water Model --> Modelo WEAP - MODFLOW.
* [Explicación del modelo - Mencionar que este está siendo desarrollado en el proyecto de Ligua Petorca (¿?)]
* Ecuación que resuelve MODFLOW.
* Imagen del modelo
* MODFLOW es un modelo de diferencias finitas (FDM). El FDM/FEM utiliza una cuadrícula/malla predefinida donde la ecuación del flujo de agua subterránea se aproxima mediante un conjunto de ecuaciones algebraicas para la cuadrícula/malla elegida en el sistema. Estos métodos son computacionalmente costosos para problemas a gran escala debido al esfuerzo de preprocesamiento requerido (Thomas et al., 2018). Sin embargo, se utilizará una arquitectura de procesamiento en paralelo que permite reducir los tiempos de simulación *(Cita dependiendo de la publicación PREPRINT que se haga)*

#### Modelo de optamización

* Plantear modelo de optimización --> Identificar las salidas de interés --> Función objetivo.   
    * Niveles de agua subterránea en pozos DGA. --> (Euclidean norm (Lingireddy, 1997), Sum of Squared Difference (SSD). Sum of the Root Mean Squared Error (SRMSE) (Patel et al., 2022))
    * Pozos colgados.
    * Variación neta del volumen almacenado por 3 periodos de tiempo.
    * No deberían haber celdas aisladas con unicos valores, es decir, si se escoge un valor debe tener una celda adyacente como mínimo con el mismo valor.
* Restricciones
    * Restricciones implícitas:
        Mencionar también la ecuación del flujo de aguas subterráneas para un acuífero en tres dimensiones (depende de las condiciones del acuífero). Estas ecuaciones son funciones implícitas del conjunto de parámetros del acuífero (variables de decisión) y pueden denominarse restricciones implícitas (Lingireddy, 1997).
    * Restricciones explícitas:
        * Establecer el rango de valores en los que se moverán las variables de decisión (Conductividad hidráulica, rendimiento y almacenamiento específico). Serían 36 variables de decisión (Kx, Kz y Sy). Estos valores se establecen en función de estudios geológicos en la zona (citar carta geológica de la zona, guía DGA, 2019).
        * MODFLOW Cell Head no crezca en el tiempo.
        * MODFLOW Cell Head no tenga caídas abruptas en primeros años.
        * MODFLOW Cell Head no tenga caídas mayores a más de 90 metros.

    *En el estudio desarrollado por Lingireddy (1997) se emplea un enfoque de doble nivel para satisfacer las restricciones implícitas del sistema. En este enfoque, las restricciones se satisfacen fuera del marco de optimización. La ventaja de este enfoque es que es posible desarrollar un modelo de optimización generalizado adecuado para problemas de estado estacionario o no estacionario. Además, al desacoplar las restricciones implícitas del sistema del modelo de optimización, es posible utilizar métodos de evaluación de funciones aproximadas, como redes neuronales, en lugar de métodos rigurosos pero computacionalmente intensivos de elementos finitos o diferencias finitas.* (Sin embargo se puede usar un modelo de elementos finitos)

#### Convolución
* 12 máscaras, cada una representa un SHAC (5 Petorca y 7 La Ligua). Considerar que dentro de cada máscara hay una variación interna.
* Considerar tamaño de la máscara (i), kernel (k), stride y zero padding.

#### Study area (Podría ir después de explicar Convolución)
* Características semi áridas de las cuencas.

## Results
* Presentar un mapa del comportamiento de la generación de variables de decisión vs el error [Ejemplo1](/Paper/EjemplosResultados/Captura1.PNG).
* Valores observados vs simulados en diferentes pozos (¿Se puede en simulación transiente?) [Ejemplo2](/Paper/EjemplosResultados/Captura2.PNG).
* Boxplot de los valores de las variables de decisión en las generaciones, para evalular la estabilidad (¿Cómo se haría si son diferentes?) [Ejemplo3](/Paper/EjemplosResultados/Captura3.PNG)
* ¿Existirá mapa de isobaras de los acuíferos de La Ligua y Petorca?
* Comparación de parámetros hidráulicos obtenidos por bombeo o geología de la zona [Ejemplo4](/Paper/EjemplosResultados/Captura4.PNG)
* Comparación de tiempos de ejecución, convergencia [Ejemplo5](/Paper/EjemplosResultados/Captura5.PNG)


## Bibliography

* Bateni, Sayed & Mortazavi-naeini, Mohammad & Ataie-Ashtiani, Behzad & Jeng, Dong-Sheng & Khanbilvardi, R.. (2015). Evaluation of Methods for Estimating Aquifer Hydraulic Parameters. Applied Soft Computing. 28. 10.1016/j.asoc.2014.12.022. 
* Carrera, J., Alcolea, A., Medina, A. et al. Inverse problem in hydrogeology. Hydrogeol J 13, 206–222 (2005). https://doi.org/10.1007/s10040-004-0404-7
* Eberhart R , Kennedy J . A new optimizer using particle swarm theory. In: Proceedings of the sixth international symposium on micro machine and human science. IEEE; 1995. p. 39–43. Oct 4 .
* A. Erdeljan, D. Capko, S. Vukmirovic, D. Bojanic, V. Congradac. Distributed pso algorithm for data model partitioning in power distribution systems. J. Appl. Res. Technol., 12 (5) (2014), pp. 947-957
* J. Kennedy and R. Eberhart, “Particle swarm optimization“, In: Proceedings of the 1995 IEEE International. Conference on Neural Networks (ICNN), IEEE Service Center, Piscataway, New Jersey, vol.4, pp.1942–1948, 1995.
* Lakshmi Prasad K, Rastogi AK (2001) Estimating net aquifer recharge and zonal hydraulic conductivity values for Mahi Right Bank Canal project area, India by genetic algorithm. Journal of Hydrology 243:149–161. https:// doi. org/ 10. 1016/ S0022- 1694(00) 00364-4
* Liu et al. (2020). Simulation of regional groundwater levels in arid regions using interpretable machine learning models. https://doi.org/10.1016/j.scitotenv.2022.154902
* Patel, S., Eldho, T.I., Rastogi, A.K. et al. Groundwater parameter estimation using multiquadric-based meshfree simulation with covariance matrix adaptation evolution strategy optimization for a regional aquifer system. Hydrogeol J 30, 2205–2221 (2022). https://doi.org/10.1007/s10040-022-02544-y
* SRINIVASA LINGIREDDY Assistant Professor (1998) AQUIFER PARAMETER ESTIMATION USING GENETIC ALGORITHMS AND NEURAL NETWORKS, CIVIL ENGINEERING SYSTEMS, 15:2, 125-144, DOI: 10.1080/02630259808970234
* Sanzana, P., Gironas, J., Braud, I., Hitschfeld, N., Vargas, X., Vicuña, S, Munoz, J. F., Villegas, R., Rubio, E. & Herrera, R. (2019a). Herramientas hidroinformaticas y consideraciones para modelar procesos superficiales y subterráneos acoplados mediante WEAP-MODFLOW. XXVIII Congreso LatinoAmericano de Hidráulica. Recuperado de: https://hal.archives-ouvertes.fr/hal-02023789
* Sanzana, P., Gironas, J., Braud, I., Muñoz, J. F., Vicuña, S, Reyes-Paecke, S., La Barrera, F. de, Branger, F., Rodríguez, F., Vargas, X., Hitschfeld, N. & Hornazábal, S. (2019b). Impact of Urban Growth and High Residential Irrigation on Streamflow and Groundwater Levels in a Peri‐Urban Semiarid Catchment. Journal of the American Water Resources Association, 55(3), 720–739. doi.org/10.1111/1752-1688.12743
* A. Thomas, P. Majumdar, T.I. Eldho, A.K. Rastogi (2018). Simulation optimization model for aquifer parameter estimation using coupled meshfree point collocation method and cat swarm optimization. Eng. Anal. Boundary Elem., 91 (2018), pp. 60-72

