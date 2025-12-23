# Comparativa Factory vs Prototype en IaC

## ¿Cuándo elegir Factory?
El patrón Factory es ideal cuando necesitas crear recursos de infraestructura con una estructura estándar y pocos cambios entre instancias. Es útil para IaC cuando los objetos a crear son simples, homogéneos y no requieren personalización profunda. Factory centraliza la lógica de creación, facilita la extensión y el mantenimiento, y permite controlar la inicialización de los recursos (por ejemplo, asignando triggers o identificadores únicos).

**Ventajas:**
- Simplicidad y claridad en la creación de objetos.
- Menor consumo de memoria, ya que no se realizan copias profundas.
- Fácil de mantener y extender para nuevos tipos de recursos.

**Desventajas:**
- Menos flexible para personalizaciones complejas.
- Si los recursos requieren muchas variantes, la lógica de la fábrica puede volverse compleja.

## ¿Cuándo elegir Prototype?
El patrón Prototype es preferible cuando necesitamos crear múltiples instancias similares pero con variaciones específicas, o cuando los objetos a clonar son costosos de construir desde cero. En IaC, Prototype permite clonar una plantilla base y aplicar mutaciones (mutators) para personalizar cada instancia, evitando la duplicación de código y facilitando la generación de configuraciones complejas.

**Ventajas:**
- Permite personalizaciones profundas y flexibles.
- Reduce la duplicación de código para recursos similares.
- Útil cuando la creación de un recurso es costosa o involucra muchos parámetros.

**Desventajas:**
- El uso de `deepcopy` puede ser costoso en memoria y tiempo para objetos grandes.
- Mayor complejidad en la gestión de mutators y plantillas.

## Costos y Mantenimiento
- **Factory:** Bajo coste de memoria y CPU, ideal para recursos simples y homogéneos. El mantenimiento es sencillo mientras la lógica de creación no crezca demasiado.
- **Prototype:** Mayor coste de memoria por las copias profundas, pero facilita la personalización y escalabilidad. El mantenimiento puede ser más complejo si hay muchos mutators o plantillas.

Por lo que podemos decir que podemos usar Factory para IaC cuando la creación es simple y estandarizada. Prefiere Prototype cuando necesitas variaciones eficientes y personalización avanzada. En proyectos grandes, una combinación de ambos patrones puede ser la mejor estrategia.
