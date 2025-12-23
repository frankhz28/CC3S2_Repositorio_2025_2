# Actividad14 - CC3S2

Este repositorio agrupa la solucion de la Actividad 14, estructurada en tres fases (Fase1, Fase2 y Fase3). Cada fase contiene ejercicios enfocados en la aplicación de patrones de diseño a Infraestructura como Código (IaC), generación de archivos JSON para Terraform y la validación mediante pruebas y ejemplos prácticos.

### Estructura principal

- `Fase1/` — Documentación y entregables conceptuales:
    - Contiene la explicación de los patrones (Singleton, Factory, Prototype, Composite, Builder) y diagramas/entregables que muestran el diseño de la solución.
    - Archivos clave: `Entregable_Fase1.md`, diagramas UML en `Diagramas_UML/`.
    
    **Ejemplo de diagrama UML (Flujo):**
    
    ![Diagrama Singleton](Fase1/Diagramas_UML/Flujo_Factory_Prototype_Composite_Builder.png)

- `Fase2/` — Implementaciones prácticas por ejercicio (código que genera ejemplos `.tf.json`):
    - `Ejercicio2.1/` — `singleton.py`: metaclase `SingletonMeta` y `ConfigSingleton` con método `reset()`, script y validación.
    - `Ejercicio2.2/` — `factory.py`: `TimestampedNullResourceFactory` que construye bloques `null_resource` con timestamp formateado, script y validación.
    - `Ejercicio2.3/` — `prototype.py`: clonación de prototipos y mutators que añaden bloques `local_file`, script y validación.
    - `Ejercicio2.4/` — `composite.py`: composición de módulos (`CompositeModule`) con soporte para submódulos, script y validación.
    - `Ejercicio2.5/` — `builder.py`: `InfrastructureBuilder` que orquesta Factory+Prototype+Composite para exportar `main.tf.json` con grupos anidados, script y validación.

- `Fase3/` — Documentos y análisis:
    - `Comparativa_Factory_vs_Prototype.md`: análisis conceptual y comparativas.

#### Artefactos generados

- Archivos `.tf.json` de ejemplo pueden colocarse en subcarpetas `terraform/` dentro de cada ejercicio si se desea.
- Los artefactos generados no son necesarios para el código fuente y pueden regenerarse con los scripts incluidos.

