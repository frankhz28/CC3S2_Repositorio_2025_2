# Timeout aplicado a tareas críticas

- Archivo: `dags/etl_pipeline.py`
- Cambio: se agregó `execution_timeout=timedelta(minutes=5)` a la tarea `extract`.
- Razón: evitar colgados. 5 min es razonable para fuentes locales/CSV. Si se excede, la tarea falla de forma explícita, acelera diagnóstico y evita consumo infinito.
- Impacto: el scheduler marca la tarea como `failed` si supera el timeout, reintentos siguen política del DAG (si aplica).
