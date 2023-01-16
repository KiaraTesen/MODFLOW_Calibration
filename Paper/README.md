# Estructura de paper

## Keywords
* Particle Swarm Optimization
* Convolutional Neural Networks (¿?)
* Hydraulic Parameters
* Aquifers
* Optimization (¿?)

## Introducción
* Antecedentes a calibración de PH de un acuífero.
    En la gestión integrada de recursos hídricos resulta muy importante el entendimiento de las aguas subterráneas

* Problema a resolver¨--> Objetivo y vació en el conocimiento.

    ### Objetivo principal
    * Calibración de parámetros hidráulicos de un acuífero utilizando algorítmos bioinspirados.
    ### Objetivo específco
    * Optimizar la calibración de un modelo subterráneo utilizando PSO (Particle Swarm Optimization) y Convolución
    * Calibrar paramétros hidráulicos (variables de decisión): 
        * Conductividad hidráulica (Kx y Kz) --> Considerando Ky = Kx
        * Rendimiento específico (Sy) --> Considerando que Almacenamiento específico (Ss) = Sy / 100
        * Supuesto: No hay variación de los parámentros en el tiempo. Limitación del programa.
    * Calcular la incertidumbre asociada a los valores de las variables de decisión.
    * Definir las funciones de pérdida.
    * Metodología aplicada a un acuífero real --> Ligua - Petorca, Chile central.

* PSO y Convolución --> ¿Por qué PSO y no un genético? --> Reducción del tiempo y trabaja en método asíncrono, teniendo en cuenta que contamos con un modelo que utiliza una arquitectura de modelación paralelizada.

## Data and  Methodology
### Study area

### Methodology
* Modelo WEAP - MODFLOW.
* Establecer el rango de valores en los que se moverán las variables de decisión.
* Identificar las salidas de interés.
    * Niveles de agua subterránea en pozos DGA.
    * Pozos colgados.
    * MODFLOW Cell Head no crezca en el tiempo.
    * MODFLOW Cell Head no tenga caídas abruptas en primeros años.
    * MODFLOW Cell Head no tenga caídas mayores a más de 90 metros.
    * Variación neta del volumen almacenado por 3 periodos de tiempo.
* Restricciones

## Bibliography



