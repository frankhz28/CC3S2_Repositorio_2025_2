### Actividad: Escribiendo infraestructura como código en un entorno local con Terraform

#### Fase 0: Preparación 

1. **Revisa** el [laboratorio 5](https://github.com/kapumota/Curso-CC3S2/tree/main/labs/Laboratorio5)  :

   ```
   modules/simulated_app/
     ├─ network.tf.json
     └─ main.tf.json
   generate_envs.py
   ```
2. **Verifica** que puedes ejecutar:

   ```bash
   python generate_envs.py
   cd environments/app1
   terraform init
   ```
3. **Objetivo**: conocer la plantilla base y el generador en Python.

####  Fase 1: Expresando el cambio de infraestructura

* **Concepto**
Cuando cambian variables de configuración, Terraform los mapea a **triggers** que, a su vez, reconcilian el estado (variables ->triggers ->recursos).

* **Actividad**

  - Modifica en `modules/simulated_app/network.tf.json` el `default` de `"network"` a `"lab-net"`.
  - Regenera `environments/app1` con `python generate_envs.py`.
  - `terraform plan` observa que **solo** cambia el trigger en `null_resource`.

* **Pregunta**

  * ¿Cómo interpreta Terraform el cambio de variable?

    Primero hace una comparacion al ejecutar terraform plan, lee el archivo main.tf.json actualizado donde network ahora es "lab-net".

    Luego revisa su archivo de **memoria** `terraform.tfstate` y ve que, la última vez que se aplicó, el valor de network era **net1**.

    Ve que el valor no solo cambió, sino que cambió dentro de un bloque triggers lo que le da la señal inequívoca: "El valor que vigilo ha cambiado, por lo tanto, este recurso (null_resource.app1) está desactualizado y debo forzar su actualización".

  * ¿Qué diferencia hay entre modificar el JSON vs. parchear directamente el recurso?

    Modificar el JSON es la forma correcta. Aqui estás cambiando el **plano** (la fuente de la verdad). El cambio es permanente, se puede guardar en Git y es reproducible. Cuando ejecutamos `terraform apply`, Terraform **construye** la realidad para que coincida con el plano.


    Mientras que parchear el recurso se refiere a un cambio manual. Esto crea una **desviación** (drift), porque el "mundo real" ya no coincide con el **código** y la próxima vez que alguien ejecute `terraform apply`, Terraform verá la diferencia y revertirá el parche manual para forzar que la realidad vuelva a coincidir con el código.

  * ¿Por qué Terraform no recrea todo el recurso, sino que aplica el cambio "in-place" **(~)**?

    Terraform es lo suficientemente inteligente como para saber que no necesita destruir todo y empezar de cero. Sabe que el null_resource sigue siendo el mismo; lo único que cambió es el valor de un argumento (el trigger). Si el cambio fuera destructivo (por ejemplo, cambiar el tipo de instancia de un servidor), Terraform mostraría un -/+ replace (destruir y crear).

    Como el cambio es solo en triggers, Terraform simplemente actualiza el valor en su tfstate y, debido a que es un trigger, vuelve a ejecutar la acción del provisioner. Es la forma más eficiente de aplicar el cambio.

  * ¿Qué pasa si editas directamente `main.tf.json` en lugar de la plantilla de variables?

      Seria un parche manual, estariamos rompiendo el flujo de IaC. Seria temporal y la próxima vez que alguien o un sistema de CI/CD ejecute python generate_envs.py, el cambio manual será completamente borrado y sobrescrito por la plantilla del script

#### Procedimiento

1. En `modules/simulated_app/network.tf.json`, cambia:

   ```diff
     "network": [
       {
   -     "default": "net1",
   +     "default": "lab-net",
         "description": "Nombre de la red local"
       }
     ]
   ```
2. Regenera **solo** el app1:

   ```bash
   python generate_envs.py
   cd environments/app1
   terraform plan
   ```

   Observa que el **plan** indica:

   > \~ null\_resource.app1: triggers.network: "net1" -> "lab-net"

#### Fase 2: Entendiendo la inmutabilidad

#### A. Remediación de 'drift' (out-of-band changes)

1. **Simulación**

   ```bash
   cd environments/app2
   # edita manualmente main.tf.json: cambiar "name":"app2" ->"hacked-app"
   ```
2. Ejecuta:

   ```bash
   terraform plan
   ```

    Verás un plan que propone **revertir** ese cambio.
3. **Aplica**

   ```bash
   terraform apply
   ```
    Y comprueba que vuelve a "app2".
   

#### B. Migrando a IaC

* **Mini-reto**
 1. Crea en un nuevo directorio `legacy/` un simple `run.sh` + `config.cfg` con parámetros (por ejemplo, puertos, rutas).

    ```
     echo 'PORT=8080' > legacy/config.cfg
     echo '#!/bin/bash' > legacy/run.sh
     echo 'echo "Arrancando $PORT"' >> legacy/run.sh
     chmod
     ```
  2. Escribe un script Python que:

     * Lea `config.cfg` y `run.sh`.
     * Genere **automáticamente** un par `network.tf.json` + `main.tf.json` equivalente.
     * Verifique con `terraform plan` que el resultado es igual al script legacy.

#### Fase 3: Escribiendo código limpio en IaC 

| Conceptos                       | Ejercicio rápido                                                                                               |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| **Control de versiones comunica contexto** | - Haz 2 commits: uno que cambie `default` de `name`; otro que cambie `description`. Revisar mensajes claros. |
| **Linting y formateo**                     | - Instala `jq`. Ejecutar `jq . network.tf.json > tmp && mv tmp network.tf.json`. ¿Qué cambió?                 |
| **Nomenclatura de recursos**               | - Renombra en `main.tf.json` el recurso `null_resource` a `local_server`. Ajustar generador Python.           |
| **Variables y constantes**                 | - Añade variable `port` en `network.tf.json` y usarla en el `command`. Regenerar entorno.                     |
| **Parametrizar dependencias**              | - Genera `env3` de modo que su `network` dependa de `env2` (por ejemplo, `net2-peered`). Implementarlo en Python.    |
| **Mantener en secreto**                    | - Marca `api_key` como **sensitive** en el JSON y leerla desde `os.environ`, sin volcarla en disco.           |

#### Fase 4: Integración final y discusión

1. **Recorrido** por:

   * Detección de drift (*remediation*).
   * Migración de legacy.
   * Estructura limpia, módulos, variables sensibles.
2. **Preguntas abiertas**:

   * ¿Cómo extenderías este patrón para 50 módulos y 100 entornos?
  
     Para escalar a decenas o cientos de módulos y entornos, es clave mantener los módulos enfocados en una sola responsabilidad y bien versionados. Se recomienda centralizar la gestión de módulos en un repositorio interno, permitiendo reutilización y control de versiones. La configuración específica de cada entorno puede manejarse con archivos de variables (`.tfvars`) o capas de overlays para evitar duplicidad. La automatización es fundamental: pipelines de CI/CD deben encargarse de validar, formatear y aplicar los cambios, además de generar artefactos de los módulos. Es importante definir convenciones claras para nombres, etiquetas y límites de recursos, así como monitoreo y documentación para facilitar la operación y el mantenimiento.

   * ¿Qué prácticas de revisión de código aplicarías a los `.tf.json`?
     
     La validación debe realizarse tanto con herramientas de formato y sintaxis (`jq`, `terraform validate`), como con linters y analizadores de seguridad (`tflint`, `tfsec`). Es preferible revisar el código fuente que genera los JSON, en vez de los archivos generados directamente. Los hooks de pre-commit y la integración continua ayudan a detectar errores antes de que lleguen al repositorio. También es importante asegurarse de que no se filtren secretos ni se modifiquen recursos críticos sin revisión adecuada.

   * ¿Cómo gestionarías secretos en producción (sin Vault)?
     
     Para proteger secretos en producción, lo ideal es utilizar servicios de gestión de secretos del proveedor de nube cuando estén disponibles, o bien cifrar las variables sensibles y almacenarlas fuera del código fuente, por ejemplo en variables de entorno o sistemas de CI/CD. El acceso a estos secretos debe estar restringido y auditable, y es recomendable rotar las claves periódicamente. Además, el estado remoto de Terraform debe estar cifrado y protegido.

   * ¿Qué workflows de revisión aplicarías a los JSON generados?
     
     El proceso debe incluir la regeneración automática de los archivos JSON en la integración continua, comparando los resultados con los cambios propuestos en el commit. Antes de aplicar cambios en producción, se debe ejecutar `terraform plan` y revisar el diff, requiriendo aprobación manual para cambios sensibles. La validación y los análisis de seguridad deben ser automáticos y ejecutarse antes de cualquier fusión a la rama principal.
     