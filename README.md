# Title
A Hybrid Approach of Convolutional Layers and Distributed Bio-inspired Algorithms with an Integrated Water Management Model to Groundwater Parameters Estimation

# Introducción (Extensión ~ 1 hoja máx)
Las aguas subterráneas juegan un rol muy importante en la Gestión Integrada de Recursos Hídricos (GIRH). Siendo aún más relevante en el balance hídrico en zonas donde el recurso superficial es escaso \citep{Liuetal2022}. Por esta razón, en la GIRH, cada vez se ha hecho más necesario el uso de herramientas de modelación que permitan simplificar, optimizar y entender los distintos procesos que ocurren en las cuencas y acuíferos. Por tanto, existen diferentes investigaciones que han acoplado programas computacionales que modelan sistemas superficiales y subterráneos \citep{Baileyetal2016, Sanzanaetal2019, ZhangandChui2020}. Dentro de los más usados está el software WEAP (Water Evaluation and Planning System) \citep{Yatesetal2005a, Yatesetal2005b}, que permite representar los procesos involucrados en la dinámica de una cuenca (e.g. distribución y disponibilidad del recurso hídrico), junto a MODFLOW \citep{Harbaughetal2000}, que permite modelar el flujo de aguas subterráneas. La ventaja del acople entre WEAP y MODFLOW es que, según la configuración establecida, permite un intercambio bidireccional de flujos en cada paso de tiempo, donde los resultados de WEAP se cargan en los archivos de entrada MODFLOW, y viceversa \citep{Sanzanaetal2019}. Esta integración se realiza con la finalidad de estudiar la disponibilidad hídrica superficial y subterránea, y su adecuado aprovechamiento \citep{Porhemmatetal2019}.

En la GIRH se requiere de una adecuada modelación de los sistemas de aguas subterráneas, lo que depende de un buen conocimiento de los parámetros hidrogeológicos del acuífero, como la conductividad hidráulica, transmisividad, coeficiente de almacenamiento, rendimiento específico y la tasa de recarga del acuífero \citep{LakshmiPrasadAndRastogi2001}. Sin embargo, estos parámetros comunmente necesitan ser estimados ya que no son fáciles de medir directamente pues requieren considerables recursos humanos y económicos \citep{Batenietal2015}. En los últimos años, investigadores han adoptado el modelado inverso de aguas subterráneas como un enfoque matemático válido para estimar los parámetros de los acuíferos \citep{Carreraetal2005, HendricksFranssenetal2009, Mohairetal2017, Pateletal2022}. En este sentido, se utilizan Simulation optimization (SO) models, en donde los parámetros distribuidos se asignan a un modelo matemático con condiciones de contorno conocidas, cuyos resultados alimentan al modelo de optimización, el cual tiene el objetivo de asegurar la minimización de errores entre las variables observadas y simuladas para obtener valores óptimos de los parámetros hidráulicos \citep{LakshmiPrasadAndRastogi2001, Pateletal2022}. 

Los modelos de optimización utilizan métodos tradicionales basados en gradientes, por ejemplo, the steepest descent method, conjugate gradient method, Gauss–Newton method \citep{Cigizoglu2005, Meza2010, Qinetal2018}, among others; y métodos no tradicionales, como los algoritmos bioinspirados , por ejemplo, Genetic Algorithm, Particle Swarm Optimization, Simulated Annealing, Differential Evolution, among others \citep{Gauretal2011, Huangetal2008, Yang2014}. La desventaja de los algorítmos basados en gradientes es que pueden dar como resultado valores óptimos locales en lugar de globales debido a la falta de convexidad inherente en los modelos de acuíferos, ya que la ecuación del modelo de flujo puede ser lineal con respecto a una variable de estado, que a su vez es altamente no lineal con respecto a los parámetros del sistema \citep{LakshmiPrasadAndRastogi2001, Batenietal2015}. Por tanto, para abordar estos inconvenientes (*shortcomings*), lot of work related to solve GW problems, aplican los algoritmos evolutivos, ya que pueden manejar problemas altamente no lineales y convergen al óptimo global en lugar del local \citep{Batenietal2015}. Sin embargo, estos métodos son computacionalmente costosos para problemas a gran escala, como lo son los problemas de GIRH evaluados mediante un Integrated Water Management Model (IWMM), debido al esfuerzo de preprocesamiento requerido. 

Por lo antes expuesto, the main objective of this research is the calibration of hydraulic parameters of an aquifer using a hybrid and asynchronous approach of convolutional layers and distributed bio-inspired algorithms with an integrated water management model. Por tanto, se plantea a SO model, en donde se evalúan modelos de optimización que utilizan la combinación de dos algorítmos bioinspirados, Particle Swarm Optimization (PSO) and Differential Evolution (DE) con las Convolutional Layers para la estimación adecuada de los parámetros hidráulicos de un acuífero. Mientras que la simulación del sistema subterráneo se realiza con un IWMM (WEAP-MODFLOW) para lograr una mejor representación de los precesos de recarga y descarga del sistema. 

PSO es un algoritmo evolutivo estocástico propuesto por Eberhart y Kennedy (\citeyear{EberhartandKennedy1995}) and has become one of the most used swarm-intelligence-based algorithms in different research areas \citep{Erdeljanetal2014, SanchezGarciaetal2019, Thomasetal2018} due to its simplicity and flexibility \citep{Yang2014}. Asimismo, DE is a vector-based metaheuristic algorithm developed by Storn and Price (\citeyear{StornandPrice1995}), which has some similarity to pattern search and genetic algorithms due to its use of crossover and mutation \citep{Yang2014}. Investigaciones recientes han aplicado ambos algorítmos de manera distribuida, [Se sacaría lo que puse en la descripción de DPSO y DDE?]. Además se plantea utilizar CL como proceso de filtrado de los paámetros hidráulicos a calibrar, por tanto, las variables de decisión serán los valores que tomen los kernel (qué es el kernel).

Finally, a simplified synthetic model is considered as a first approach that will allows validating the proposed DPSO-CL and DDE-CL algorithms. Sin embargo, como se mencionó anteriormente, trabajar con un modelo integrado y algoritmos de optimización genera un gasto computacional alto, por lo que se utilizará una arquitectura de procesamiento en paralelo que permite reducir los tiempos de simulación, aplicando los algoritmos en diferentes máquinas que comunican sus resultados entre sí o a una máquina server, tras cada generación, dependiendo de la consifugración del algorítmo. 

-
[Vacío en el conocimiento a abordar - RECALCAR CONVOLUCION Y ALGORITMOS]



[Idea de cierre]


......


......
......
......

Sin embargo, en la presente investigación se hará uso también de Convoluciones [ ---- Previamente poner antecedentes de las convoluciones en ciencias físicas ---- luego explicar porqué es conveniente usarlas juntas ---- ]


El algoritmo PSO distribuido se basa en la búsqueda de soluciones disponibles en el espacio paralelo [25]. --> Paper que hablaa de Tsync

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