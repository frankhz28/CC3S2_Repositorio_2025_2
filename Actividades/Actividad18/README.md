# Evidencia de Laboratorio: DevSecOps con Docker y Airflow

## 1. Resumen
Implementación de prácticas DevSecOps en un entorno ETL usando Docker y Airflow. Se documentan controles, validaciones y hallazgos de seguridad.

## 2. Evidencias y Validaciones

| Control / Práctica              | Evidencia / Archivo                | Descripción / Validación                                                                 |
|----------------------------------|------------------------------------|-----------------------------------------------------------------------------------------|
| Construcción de Imágenes         | `00_build.txt`                     | Build exitoso de imágenes Docker                                                        |
| Topología y Red                  | `04_topologia.md`, `05_net_inspect.txt` | Red `backend` aislada, mínima exposición de puertos                                     |
| Estado de Salud                  | `10_health_status.txt`             | Servicios reportan `healthy` vía healthchecks                                           |
| Arranque Ordenado                | `10_compose_diff.md`               | Uso de `depends_on` y healthchecks para inicialización controlada                       |
| Usuario No-Root                  | `12_user_check.txt`                | Contenedor app ejecuta como `etluser` (UID 10001), no como root                         |
| Manejo de Variables/Secretos     | `13_env_audit.txt`                 | Inyección segura de configuración y redacción de secretos                               |
| Límites de Recursos              | `docker-compose.yml`               | Restricciones de CPU y memoria para prevenir DoS                                        |
| SBOM (Inventario Software)       | `21_sbom.spdx.json`, `21_sbom_fs.spdx.json` | Inventario generado con Syft                                                           |
| Escaneo de Vulnerabilidades      | `22_scan.txt`                      | Reporte de CVEs detectados con Grype                                                    |
| Plan de Remediación              | `23_cve_plan.md`                   | Acciones propuestas para CVEs críticos                                                  |
| Documentación de DAG             | `30_dag_resumen.md`                | Descripción y validación del pipeline ETL                                               |
| Ejecución de DAG                 | `31_dag_run.txt`                   | Evidencia de ejecución exitosa                                                          |
| Timeout y Resiliencia            | `32_timeout_diff.md`               | Implementación de `execution_timeout` para evitar tareas zombies                        |
| Pruebas Funcionales              | `20_tests.txt`                     | Resultados de pruebas con pytest                                                        |

## 3. Reproducibilidad

1. Preparar entorno:
    ```bash
    cp .env.example .env
    mkdir -p airflow/logs airflow/dags app/data
    chmod -R 777 airflow/logs
    ```
2. Construir e inicializar:
    ```bash
    make build
    make reset-init
    ```
3. Arrancar servicios:
    ```bash
    make up
    ```
4. Verificar en `http://localhost:8080` (admin/admin).

## 4. Decisiones de Seguridad Clave

- **Principio de Menor Privilegio:** Usuario `etluser` (UID 10001) en app.
- **Aislamiento de Red:** Red `backend` bridge, mínima exposición de puertos.
- **Límites de Recursos:** CPU y memoria limitados en `docker-compose.yml`.
- **Healthchecks:** Verificaciones de salud para tráfico seguro.

## 5. Pruebas y Gates de Seguridad

- Pruebas funcionales: `make test`
- SBOM: `make sbom`
- Escaneo de vulnerabilidades: `make scan`

## 6. Retos

- Permisos de volúmenes: Ajuste de permisos para logs de Airflow.
- Conectividad DB: Uso de healthchecks para dependencias.
- Ejecución de DAGs: Corrección de IDs y validación manual.
- Resiliencia: Timeout en DAG para evitar tareas zombies.