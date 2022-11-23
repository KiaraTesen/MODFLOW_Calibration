# MODFLOW Parameters Calibration

## Objetivo principal
* Calibración de parámetros hidráulicos de un acuífero utilizando algorítmos bioinspirados.

## Objetivo específco
* Optimizar la calibración de un modelo subterráneo utilizando PSO (Particle Swarm Optimization)
* Calibrar paramétros hidráulicos (variables de decisión): 
    * Conductividad hidráulica (Kx y Kz) --> Considerando Ky = Kx
    * Rendimiento específico (Sy) --> Considerando que Almacenamiento específico (Ss) = Sy / 100
    * Supuesto: No hay variación de los parámentros en el tiempo. Limitación del programa.
* Calcular la incertidumbre asociada a los valores de las variables de decisión.
* Definir las funciones de pérdida.
* Metodología aplicada a un acuífero real --> Ligua - Petorca, Chile central.

## Metodología
* Modelo WEAP - MODFLOW.
* Establecer el rango de valores en los que se moverán las variables de decisión.
* Identificar las salidas de interés.
    * Niveles de agua subterránea en pozos DGA.
    * Pozos colgados.
    * MODFLOW Cell Head no crezca en el tiempo.
    * Variación neta del volumen almacenado por 3 periodos de tiempo.
* Restricciones

