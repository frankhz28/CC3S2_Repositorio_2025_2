# Resumen operativo del DAG: etl_pipeline

## Tareas y dependencias
- **extract**: Lee datos desde el archivo de entrada definido por la variable de entorno `ETL_INPUT`.
- **transform**: Procesa y transforma los datos extraídos.
- **load**: Carga los datos transformados en el destino definido por `ETL_OUTPUT`.

**Dependencias:**
- El flujo es secuencial: `extract >> transform >> load`.
- Si alguna tarea falla, las siguientes no se ejecutan.

## Configuración por variables de entorno y conexiones
- **Variables de entorno principales:**
  - `ETL_INPUT`: Ruta al archivo de entrada (ej: `/app/data/input.csv`).
  - `ETL_OUTPUT`: Ruta al archivo de salida (ej: `/app/data/output.csv`).
  - `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`: Credenciales y base de datos destino si se usa Postgres.

## Logs y verificación de éxito/fallo
- **Dónde se registran logs:**
  - Los logs de cada tarea se almacenan en la interfaz de Airflow (UI) y en el volumen de logs del contenedor Airflow (`airflow/logs/`).
  - Consultamos logs con: `docker compose logs airflow-scheduler` y `airflow-webserver`.
- **Cómo detectar éxito/fallo:**
  - En la UI de Airflow, cada tarea muestra su estado (verde: éxito, rojo: fallo).
  - En consola, verificamos con:
    - `airflow dags list-runs -d etl_pipeline` para ver el estado global del DAG.
    - `airflow tasks list etl_pipeline --tree` para ver la estructura y dependencias.
    - Buscar en los logs la línea `Task ... succeeded` para cada tarea.
  - El DAG se considera exitoso si todas las tareas terminan en estado `success`.

## Ejecucion y monitoreo
- Para disparar el DAG manualmente:
  1. Accede al contenedor scheduler: `docker compose exec airflow-scheduler bash`
  2. Ejecuta: `airflow dags trigger etl_pipeline`
  3. Monitorea el estado en la UI o con los comandos mencionados anteriormente en Logs y verificacion.
