# Estructura de paper

## Keywords
* Particle Swarm Optimization --> Genético o bio-inspirado? Son lo mismo?
* Convolutional Neural Networks (¿?)
* Aquifer Hydraulic Parameters
* Optimization (¿?)
* Simulation - Optimization model

## Introducción
* Antecedentes a calibración de PH de un acuífero.

    Las aguas subterráneas juegan un rol muy importante en la Gestión Integrada de Recursos Hídricos (GIRH). Siendo aún más relevante en el balance hídrico de áreas donde la dinámica río-acuífero afecta las secciones del lecho del río, o donde las alcantarillas están ubicadas debajo del nivel del agua subterránea (Sanzana et al., 2019b), o en zonas donde el recurso superficial es escaso (Liu et al., 2022). Por esta razón, cada vez se ha hecho más necesario el uso de herramientas de modelación que permitan simplificar y/u optimizar distintos procesos. En la GIRH estas labores pueden llegar a ser complicadas dependiendo de las características de la cuenca o acuífero de interés (Sanzana et al., 2019a; b). En este sentido, una adecuada modelación de los sistemas de aguas subterráneas depende de un buen conocimiento de los parámetros hidrogeológicos del acuífero, como la conductividad hidráulica, almacenamiento, rendimiento específico y la tasa de recarga del acuífero (Lakshmi Prasad y Rastogi 2001). Sin embargo, estos parámetros comunmente necesitan ser estimados ya que no son fáciles de medir directamente pues requieren considerables recursos humanos y económicos (Lakshmi Prasad y Rastogi 2001). 
    
    En los últimos años se ha adopatado el modelado inverso de aguas subterráneas como un enfoque matemático válido para estimar los parámetros de los acuíferos (Patel et al., 2022 + CITAS). En este sentido, se utilizan modelos de simulación optimización (Simulation optimization (SO) models), en donde los parámetros distribuidos se asignan a un modelo matemático con condiciones de contorno conocidas, cuyos resultados alimentan al modelo de optimización, el cual tiene el objetivo de asegurar la minimización de errores entre las variables observadas y simuladas para obtener valores óptimos y representativos de los parámetros hidráulicos (Lakshmi Prasad y Rastogi 2001; Patel et al., 2022). La simulación del sistema se realiza utilizando modelos basado en cuadrículas o mallas, modelos de diferencias finitas (FDM) o de elementos finitos (FEM); o simuladores independientes de una malla, Meshfree (Mfree).


    ---

    Hablar del modelo, considerando que es una desventaja el tiempo de modelación aunque se ha implementado una metodología de ejecución en paralelo que permite reducir los tiempos de simulación.

    Aplicaciones de PSO y Convolución en hidrología e hidrogeología.
    Una de las críticas a los algorítmos genéticos es que requieren muchas evaluaciones de funciones antes de llegar a la solución óptima superior (Lingireddy, 1997) y aunque los avances tecnológicos han hecho que esto no sea tan crítico, el problema persiste al evaluar acuíferos muy grandes (Lingireddy, 1997). [ ---- Aquí hablaría de la paralelización ---- ]

    Sin embargo, en la presente investigación se hará uso también de Convoluciones [ ---- Previamente poner antecedentes de las convoluciones en ciencias físicas ---- luego explicar porqué es conveniente usarlas juntas ---- ]

    Los algorítmos genéticos (GA) Lsolo se ocupan de problemas de optimización sin restricciones (Lingireddy, 1997). Los GA con un enfoque indirecto tienen la ventaja que es adecuado para situaciones en las que los datos disponibles son escasos (Lingireddy, 1997). DeJong(1975) recommended a high probability of crossover along with a low probability of mutation for good convergence characteristics of a genetic algorithm. Typical values of probabilities of crossover and mutation are 0.6 ~ 0.7 (0 - 1) and 0.02 ~ 0.03 (0 - 0.1) respectively (Lingireddy, 1997).


* Problema a resolver¨--> Objetivo y vació en el conocimiento.

    ### Objetivo principal
    * Calibración de parámetros hidráulicos de un acuífero utilizando algorítmos bioinspirados. [Encontrar el set de parámetros óptimos que reduzca el error (qué monitorearemos - fitness function (¿?)) entre los valores observados y simulados] --> Se plantea un modelo de simulación - optimización (SO).
    ### Objetivo específco
    * Optimizar la calibración de un modelo subterráneo utilizando PSO (Particle Swarm Optimization) y Convolución
    * Calibrar paramétros hidráulicos (variables de decisión): 
        * Conductividad hidráulica (Kx y Kz) --> Considerando Ky = Kx
        * Rendimiento específico (Sy) --> Considerando que Almacenamiento específico (Ss) = Sy / 100
        * Supuesto: No hay variación de los parámentros en el tiempo. Limitación del programa.
    * Calcular la incertidumbre asociada a los valores de las variables de decisión.
    * Definir las funciones de pérdida.
    * Metodología aplicada a un acuífero real --> Ligua - Petorca, Chile central.


* PSO (es un algoritmo de optimización estocástico ¿?) y Convolución --> ¿Por qué PSO y no un genético? --> Reducción del tiempo y trabaja en método asíncrono, teniendo en cuenta que contamos con un modelo que utiliza una arquitectura de modelación paralelizada.

## Data and  Methodology
#### Study area
* Caracteríastica de los acuíferos (área, confinado(¿? Esto también explicaría porqué el uso de NWT))
* Características semi áridas de las cuencas.

#### Integrated Managment Water Model --> Modelo WEAP - MODFLOW.
* [Explicación del modelo - Mencionar que este está siendo desarrollado en el proyecto de Ligua Petorca (¿?)]
* Ecuación que resuelve MODFLOW.
* Imagen del modelo
* MODFLOW es un modelo de diferencias finitas (FDM)

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
## Results
* Presentar un mapa del comportamiento de la generación de variables de decisión vs el error [Ejemplo1](/Paper/EjemplosResultados/Captura1.PNG).
* Valores observados vs simulados en diferentes pozos (¿Se puede en simulación transiente?) [Ejemplo2](/Paper/EjemplosResultados/Captura2.PNG).
* Boxplot de los valores de las variables de decisión en las generaciones, para evalular la estabilidad (¿Cómo se haría si son diferentes?) [Ejemplo3](/Paper/EjemplosResultados/Captura3.PNG)
* ¿Existirá mapa de isobaras de los acuíferos de La Ligua y Petorca?


## Bibliography

* Lakshmi Prasad K, Rastogi AK (2001) Estimating net aquifer recharge and zonal hydraulic conductivity values for Mahi Right Bank Canal project area, India by genetic algorithm. Journal of Hydrology 243:149–161. https:// doi. org/ 10. 1016/ S0022- 1694(00) 00364-4
* Liu et al. (2020). Simulation of regional groundwater levels in arid regions using interpretable machine learning models. https://doi.org/10.1016/j.scitotenv.2022.154902
* Patel, S., Eldho, T.I., Rastogi, A.K. et al. Groundwater parameter estimation using multiquadric-based meshfree simulation with covariance matrix adaptation evolution strategy optimization for a regional aquifer system. Hydrogeol J 30, 2205–2221 (2022). https://doi.org/10.1007/s10040-022-02544-y
* SRINIVASA LINGIREDDY Assistant Professor (1998) AQUIFER PARAMETER ESTIMATION USING GENETIC ALGORITHMS AND NEURAL NETWORKS, CIVIL ENGINEERING SYSTEMS, 15:2, 125-144, DOI: 10.1080/02630259808970234
* Sanzana, P., Gironas, J., Braud, I., Hitschfeld, N., Vargas, X., Vicuña, S, Munoz, J. F., Villegas, R., Rubio, E. & Herrera, R. (2019a). Herramientas hidroinformaticas y consideraciones para modelar procesos superficiales y subterráneos acoplados mediante WEAP-MODFLOW. XXVIII Congreso LatinoAmericano de Hidráulica. Recuperado de: https://hal.archives-ouvertes.fr/hal-02023789
* Sanzana, P., Gironas, J., Braud, I., Muñoz, J. F., Vicuña, S, Reyes-Paecke, S., La Barrera, F. de, Branger, F., Rodríguez, F., Vargas, X., Hitschfeld, N. & Hornazábal, S. (2019b). Impact of Urban Growth and High Residential Irrigation on Streamflow and Groundwater Levels in a Peri‐Urban Semiarid Catchment. Journal of the American Water Resources Association, 55(3), 720–739. doi.org/10.1111/1752-1688.12743
*

