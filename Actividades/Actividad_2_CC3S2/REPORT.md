# Actividad 2:  HTTP, DNS, TLS y 12-Factor (port binding, configuración, logs)

## 1) HTTP: Fundamentos y herramientas

1. **Levanta la app** con variables de entorno (12-Factor):
   `PORT=8080 MESSAGE="Hola CC3S2" RELEASE="v1" python3 app.py` (usa tu *venv*). 

    **Creamos el entorno virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

    **Ya dentro del entorno instalamos `flask`**
    ```bash
    pip install flask
    ```

    **Levantamos la aplicacion**
    ```bash
    PORT=8080 MESSAGE="HOLA CC3S2" RELEASE="v1" python3 app.py 
    ```
    
    ![alt text](imagenes/evidencia1_1.png)

    **Comprobamos**
        
    ![alt text](imagenes/evidencia1_1_2.png)


2. **Inspección con `curl`:**

    `curl -v http://127.0.0.1:8080/` (cabeceras, código de estado, cuerpo JSON).

    ![alt text](imagenes/evidencia1_2_1.png)

    `curl -i -X POST http://127.0.0.1:8080/` 
   
   ![alt text](imagenes/evidencia1_2_2.png)

    En la aplicación Flask solo se define la ruta `/` con el decorador `@app.route("/")` que por defecto solo acepta métodos GET y HEAD. Cuando intentamos hacer POST a la misma ruta, Flask responde con 405 Method Not Allowed.

    Por otro lado el header Allow nos indica que métodos si están permitidos para esa ruta:

    - OPTIONS: método estándar para consultar qué métodos acepta el endpoint
    - HEAD: versión sin cuerpo del GET (solo headers)
    - GET: el método que realmente implementaste en el código

   **Pregunta guía:** ¿Qué campos de respuesta cambian si actualizas `MESSAGE`/`RELEASE` sin reiniciar el proceso? 

    Ningun campo cambiaria en la respuesta JSON, esto debido a que las variables de entorno se leen una sola vez cuando el proceso inicia y se ejecutan estas líneas por lo que los valores MESSAGE y RELEASE quedan fijos en memoria durante toda la vida del proceso. Asi que si intenamos cambiar variables de entorno en la shell esto no afectara al proceso ya en ejecución, **solo afecta nuevos procesos que se lancen**.

    En el contexto **12-Factor**, este comportamiento es consistente con el principio de configuración por entorno, en donde la configuración se lee al inicio del proceso y para cambiar la configuración necesitamos reiniciar el proceso lo que garantiza comportamiento predecible y evita cambios inesperados durante ejecución

3. **Puertos abiertos con `ss`:**

   * `ss -ltnp | grep :8080` (evidencia del proceso y socket).

    ![alt text](imagenes/evidencia1_2_3.png)

    | Comando | Descripción |
    |---|---|
    | -l | Muestra solo los sockets que están en estado de escucha (_listening_). |
    | -t | Muestra solo las conexiones de tipo TCP. |
    | -n | Muestra las direcciones numéricas en lugar de resolver los nombres de _hosts_, lo que acelera la ejecución. |
    | -p | Muestra el identificador del proceso (_PID_) y el nombre del programa al que pertenece el _socket_. |

4. **Logs como flujo:** Demuestra que los logs salen por stdout (pega 2–3 líneas). Explica por qué **no** se escriben en archivo (12-Factor).

    ![alt text](imagenes/evidencia1_2_4.png)

    ¿Por que **no** se escriben en archivo (12-Factor)?

    Por el principio de **Logs = Flujos de eventos**

    - Separación de responsabilidades: La aplicación NO debe preocuparse por gestionar archivos de log. Su responsabilidad es generar eventos

    - Flexibilidad de destino: Al escribir a stdout, el entorno de ejecución decide qué hacer con los logs

    - Simplicidad: La app no necesita configurar rutas, rotación, permisos de archivos


#### 2) DNS: nombres, registros y caché

**Meta:** resolver `miapp.local` y observar TTL/caché.

1. **Hosts local:** agrega `127.0.0.1 miapp.local` (Linux y/o Windows según tu entorno).

    ![alt text](imagenes/evidencia2_1.png)

2. **Comprueba resolución:**

   `dig +short miapp.local` (debe devolver `127.0.0.1`).

    ![alt text](imagenes/evidencia2_2_1.png)

   `getent hosts miapp.local` (muestra la base de resolución del sistema).

    ![alt text](imagenes/evidencia2_2_2.png)

3. **TTL/caché (conceptual):** con `dig example.com A +ttlunits` explica cómo el TTL afecta respuestas repetidas (no cambies DNS público, solo observa).

    ![alt text](imagenes/evidencia2_3.png)

4. **Pregunta guía:** ¿Qué diferencia hay entre **/etc/hosts** y una zona DNS autoritativa? ¿Por qué el *hosts* sirve para laboratorio?

   | Aspecto | /etc/hosts | Zona DNS Autoritativa |
   |---------|------------|---------------------|
   | **Ámbito** | Solo local (una máquina) | Global (Internet) |
   | **Precedencia** | Primera consulta (prioridad alta) | Segunda consulta |
   | **Gestión** | Manual, archivo texto | Centralizada, servidores DNS |
   | **Escalabilidad** | No escalable (máquina por máquina) | Altamente escalable |
   | **Propagación** | Instantánea | Controlada por TTL |
   | **Disponibilidad** | Depende del archivo local | Alta disponibilidad/redundancia |
   | **Uso típico** | Desarrollo/testing | Producción |

   **¿Por qué /etc/hosts sirve para laboratorio?**
   - Simplicidad: no requiere configurar servidores DNS
   - Control total: cambios inmediatos sin esperar propagación
   - Aislamiento: solo afecta el entorno de desarrollo  
   - Perfecto para `miapp.local → 127.0.0.1` en testing local