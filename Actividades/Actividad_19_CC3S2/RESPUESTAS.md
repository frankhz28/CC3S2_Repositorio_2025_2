# Conceptualización de Microservicios

Una arquitectura de microservicios consiste en diseñar una aplicación como un conjunto de pequeños servicios independientes, cada uno ejecutando un proceso propio y comunicándose mediante APIs bien definidas (generalmente HTTP/REST o gRPC). Cada microservicio se enfoca en una única capacidad de negocio, puede ser desarrollado y desplegado de forma autónoma, y tiene su propio ciclo de vida. Esto permite mayor flexibilidad, escalabilidad y resiliencia frente a fallos, a costa de una mayor complejidad operativa y de integración.

**Ventajas de microservicios:**
- Aislamiento de fallos: un error en un servicio no afecta a toda la aplicación.
- Escalado granular: solo se escalan los servicios necesarios.
- Autonomía de equipos: cada equipo puede desplegar y mantener su propio servicio.

**Desventajas y retos:**
- Complejidad operativa: más servicios, más monitoreo y orquestación.
- Consistencia de datos: cada servicio puede tener su propia base de datos.
- Testing distribuido: requiere pruebas contractuales y stubs/mocks.
- Seguridad y redes: más puntos de entrada y comunicación interna.

**Mitigaciones:**
- Contratos OpenAPI, pruebas contractuales, trazabilidad (Jaeger), patrones de sagas.

**Principios de diseño:**
- DDD para delimitar servicios.
- DRY equilibrado: librerías comunes vs duplicación controlada.
- Tamaño: una capacidad de negocio por servicio.

## Empaquetado y verificación con Docker (base obligatoria)

**Base obligatoria:**
- Docker + SQLite (archivo `app.db`)
- Puerto 80 en el contenedor
- Pruebas con `pytest -q` ejecutadas dentro del contenedor

**¿Por qué SQLite y no Postgres?**
- SQLite es ideal para desarrollo y pruebas por su simplicidad (archivo único, sin servidor). Postgres es más robusto para producción, pero la base exige SQLite para facilitar la reproducibilidad y evitar dependencias externas.

**Evidencias en texto plano:**

1.  **Build**:
    ```bash
    $ make build
    docker build -t ejemplo-microservice:0.1.0 .
    [+] Building ...
    => => naming to docker.io/library/ejemplo-microservice:0.1.0
    ```

2.  **Run**:
    ```bash
    $ make run
    docker run -d -p 80:80 --name ejemplo-microservice ejemplo-microservice:0.1.0
    ...
    ```

3.  **Curl** (Probando el endpoint):
    ```bash
    $ curl -L http://localhost:80/api/items
    []
    ```

4.  **Logs**:
    ```bash
    $ docker logs ejemplo-microservice
    ...
    ```

5.  **Pytest** (Ejecutado dentro del contenedor):
    ```bash
    $ docker exec ejemplo-microservice pytest -q
    ..
    1 failed, 1 passed, 8 warnings in 0.87s
    ```

### ¿Por qué no usar latest?

El tag `latest` en Docker es ambiguo y poco predecible: no refleja una versión específica ni garantiza compatibilidad. Usar `latest` puede provocar que, al reconstruir o desplegar, se obtenga una imagen diferente a la esperada, rompiendo entornos o introduciendo errores inesperados. Por eso, es una mala práctica en entornos de producción o entrega.

### SemVer y reproducibilidad

**SemVer (Semantic Versioning - MAJOR.MINOR.PATCH)** es un estándar que permite identificar claramente la versión y los cambios de una imagen o artefacto:

*   **Reproducibilidad:** Etiquetar una imagen como `0.1.0` asegura que siempre se podrá reconstruir o desplegar exactamente el mismo artefacto, evitando sorpresas.
*   **Trazabilidad:** Permite rastrear qué cambios, correcciones o mejoras incluye cada versión, facilitando auditoría y control.
*   **Despliegues seguros:** Facilita la promoción de versiones probadas entre entornos (dev → staging → prod), usando imágenes inmutables y confiables, en vez de una `latest` que puede variar sin previo aviso.

