# Reporte de Topología de Red y Superficie de Ataque

### 1. Topología de Red Actual
El proyecto se despliega sobre una red de tipo **Bridge** generada automáticamente por Docker Compose, identificada en la inspección como `pc5soft_default` (con subred `172.18.0.0/16`). Todos los contenedores del stack (`airflow-webserver`, `postgres`, `airflow-scheduler`, `etl-app`) se conectan a esta única red plana, lo que permite una comunicación irrestricta entre ellos mediante el protocolo TCP/IP.

### 2. Servicios y Relaciones
- **Airflow Webserver y Scheduler:** Inician conexiones salientes hacia el servicio `postgres` en el puerto 5432 para la persistencia de metadatos y estado de los DAGs.
- **ETL App:** Se conecta a `postgres` para extracción/carga de datos o interactúa con la API de Airflow.
- **Postgres:** Actúa como servidor pasivo, recibiendo conexiones de los componentes de Airflow y la aplicación ETL. No inicia conexiones hacia otros contenedores.

### 3. Resolución de Nombres (DNS)
La comunicación interna no depende de direcciones IP efímeras. Docker proporciona un servidor DNS interno (en `127.0.0.11`) que permite a los servicios resolverse por su nombre de servicio definido en el `docker-compose.yml`.

### 4. Superficie Expuesta
Actualmente, la superficie de ataque expuesta al host se limita a:
- **Airflow Webserver (Puerto 8080):** Expuesto para permitir el acceso de los operadores a la interfaz gráfica (UI) y monitoreo.

**Servicios no expuestos:**
Es una práctica de seguridad crítica que servicios como `postgres` o `etl-app` **no publiquen puertos** (`ports:`) hacia el host. La base de datos solo debe ser accesible por las aplicaciones backend dentro de la red de Docker para prevenir ataques de fuerza bruta externos o fugas de datos.
