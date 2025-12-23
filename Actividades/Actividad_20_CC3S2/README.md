# Actividad 20 - CC3S2 RESUMEN

## Parte A - Mejoras en Kubernetes

### A.1. Contenedores y variables

Se reviso y mejoro los manifiestos de Kubernetes para `user-service` y `order-service`:

- Se verifica que los nombres de los contenedores sean correctos.
- La imagen ahora es parametrizable usando `IMAGE_PLACEHOLDER` para facilitar la integración con el pipeline.
- Los puertos están correctamente definidos: `8000` para `user-service` y `8001` para `order-service`.
- Variables de entorno:
  - `PORT` con el valor correspondiente.
  - `SERVICE_NAME` agregado para cada servicio.

### A.2. Probes de salud

- Se configuraron `livenessProbe` y `readinessProbe` en ambos servicios:
  - Ambas apuntan a `path: /health` y al puerto correspondiente.
  - Se ajustaron los tiempos de espera para mejorar la robustez del monitoreo.

### A.3. Recursos y seguridad

- Se añadaden límites y solicitudes de recursos:
  - `requests`: cpu: "50m", memory: "64Mi"
  - `limits`: cpu: "200m", memory: "128Mi"
- Se incorporó un `securityContext` estricto:
  - `runAsNonRoot: true`
  - `runAsUser: 1000`
  - `allowPrivilegeEscalation: false`
  - `readOnlyRootFilesystem: true`

### A.4. Namespace (opcional)

- Se recomendo el uso de un namespace dedicado (por ejemplo, `devsecops-lab11`) para aislar los recursos, aunque los manifiestos funcionan en `default` para compatibilidad.

**Archivos modificados:**
- `Laboratorio11/k8s/user-service/deployment-and-service.yaml`
- `Laboratorio11/k8s/order-service/deployment-and-service.yaml`

## Parte B - Makefile y pipeline DevOps local

### B.1. Local-first: sin proveedores nube ni registries remotos

- El flujo de trabajo se adaptado para funcionar 100% de manera local usando Minikube, sin depender de registros externos ni servicios en la nube.
- El target `build` utiliza el daemon de Docker de Minikube para que las imágenes sean accesibles directamente por el clúster.
- El flujo **recomendado** es:
  1. Construcción de la imagen local.
  2. Pruebas de integración con docker-compose.
  3. Generación de SBOM/SCA (opcional, si se cuenta con syft/grype).
  4. Despliegue en Minikube y smoke test.

### B.2. Targets mínimos del Makefile

- Se agregaron y mejoraron los siguientes targets:
  - `env`: Inicializa variables de entorno y muestra configuración.
  - `build`: Construye la imagen usando el Docker de Minikube.
  - `test`: Ejecuta pruebas de integración con docker-compose y verifica `/health`.
  - `sbom` y `scan`: Generan SBOM y escaneo de vulnerabilidades si las herramientas están disponibles.
  - `k8s-prepare`: Copia y parametriza los manifiestos para el despliegue.
  - `minikube-up`: Asegura que Minikube esté corriendo con los recursos definidos.
  - `k8s-apply`: Aplica los manifiestos al clúster y espera el rollout.
  - `smoke`: Ejecuta el script de smoke test para verificar el servicio.
  - `dev`: Flujo completo local: `env -> minikube-up -> build -> test -> k8s-prepare -> k8s-apply -> smoke`.

### B.3. Uso y mejoras de los scripts de apoyo

- `scripts/minikube_smoke.sh`: Ahora espera a que el pod esté en estado Running y realiza reintentos robustos para `/health`, asegurando limpieza del port-forward.
- `scripts/pipeline.sh`: Orquesta el pipeline mostrando mensajes claros de inicio y fin, y permite pasar parámetros de severidad y firma.
- `scripts/muestra_salidas.sh`: Muestra artefactos, SBOM, SCA, manifiestos, recursos de Kubernetes y los eventos recientes del namespace para facilitar el diagnóstico.

**Archivos modificados:**
- `Laboratorio11/Makefile`
- `Laboratorio11/scripts/minikube_smoke.sh`
- `Laboratorio11/scripts/pipeline.sh`
- `Laboratorio11/scripts/muestra_salidas.sh`

## Parte C - Evidencias y reproducibilidad

Para asegurar la trazabilidad y reproducibilidad del flujo DevOps local, se incluyeron los siguientes archivos en la carpeta `evidencia/`:

### C.1. comandos.txt
- Lista ordenada de los comandos ejecutados durante el proceso:
  - Creación/activación de entorno
  - Builds locales
  - Pruebas con docker-compose
  - Levantamiento de Minikube
  - Aplicación de manifiestos
  - Smoke tests

### C.2. kubectl-get.txt
- Salida del comando:
  ```bash
  kubectl get deploy,svc,pod -o wide
  ```
  (en el namespace utilizado, por ejemplo `default` o `devsecops-lab11`).

### C.3. smoke-tests.txt
- Salida de la ejecución de `scripts/minikube_smoke.sh` para ambos servicios:
  - `user-service` (puerto 8000)
  - `order-service` (puerto 8001)

### C.4. sbom-lista.txt (opcional)
- Listado de los archivos SBOM y SCA generados:
  - `*-sbom.json`
  - `*-grype.sarif`

Estos archivos permiten validar que el flujo es reproducible y que los servicios funcionan correctamente en un entorno local, sin dependencias externas.

---

