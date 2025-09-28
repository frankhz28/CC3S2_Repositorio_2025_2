## Actividad 4: Introducción a herramientas CLI en entornos Unix-like para DevSecOps

### Sección 1: Manejo sólido de CLI

#### Ejercicios de reforzamiento
1. Navega a `/etc`, lista archivos ocultos y redirige la salida a un archivo en tu home: `cd /etc; ls -a > ~/etc_lista.txt`.

    ![](imagenes/sesion1_1.png)

2. Usa globbing para listar todos los archivos en `/tmp` que terminen en `.txt` o `.doc`, y cuenta cuántos hay con una tubería (versión robusta): `find /tmp -maxdepth 1 -type f \( -name '*.txt' -o -name '*.doc' \) | wc -l`.

    ![](imagenes/sesion1_2.png)

3. Crea un archivo con `printf "Línea1\nLínea2\n" > test.txt`.

    ![](imagenes/sesion1_3.png)

4. (Intermedio) Redirige errores de un comando fallido (ej. `ls noexiste`) a un archivo y agrégalo a otro: `ls noexiste 2>> errores.log`.

    ![](imagenes/sesion1_4_1.png)


    Para borrados con xargs, primero haz un dry-run: `find . -maxdepth 1 -name 'archivo*.txt' | xargs echo rm`.    

    ![](imagenes/sesion1_4_2.png)    

#### Comprobación
- `nl test.txt` (muestra líneas numeradas).

    ![](imagenes/comprobacion1_1.png)

- `wc -l lista.txt` (cuenta líneas en lista.txt).

    ![](imagenes/comprobacion1_1.png)

### Sección 2: Administración básica

#### Riesgo & Mitigación en DevSecOps
Riesgo: Over-permission en usuarios/permisos puede exponer datos sensibles en contenedores o repos. 
Mitigación: Aplica `umask 027` para archivos nuevos (solo durante la sesión), evita operaciones recursivas en `/` y usa `--preserve-root` con `chown/chgrp/rm`. 
Para procesos, usa señales controladas para no interrumpir servicios críticos.

#### Marco teórico
La administración básica en Unix-like es crucial en DevSecOps para gestionar accesos seguros, monitorear procesos y servicios, y asegurar la integridad del sistema. 
- **Usuarios/Grupos/Permisos**: Controlan quién accede a qué, previniendo brechas de seguridad (principio de menor privilegio).
- **Procesos/Señales**: Monitorean y controlan ejecuciones, útil para depurar contenedores Docker o pods Kubernetes.
- **systemd**: Gestor de servicios en sistemas modernos como Ubuntu, para iniciar/parar servicios de manera segura.
- **journalctl**: Herramienta de logging para auditar eventos del sistema, esencial en investigaciones de incidentes de seguridad.

Estos permiten configuraciones seguras en pipelines DevSecOps, como rotación de credenciales o monitoreo de anomalías.

#### Explicaciones paso a paso
1. **Usuarios/Grupos/Permisos**:
   - `whoami`: Muestra tu usuario actual.
   - `id`: Muestra UID, GID y grupos.
   - Crear usuario (con sudo): `sudo adduser nuevouser` (en entornos compartidos/multi-usuario, hazlo solo en WSL o VM personal.
     Alternativa mock: crea un directorio `mkdir mockuser` y simula `chown` con tu usuario actual para no alterar cuentas reales).
   - Grupos: `sudo addgroup nuevogrupo; sudo usermod -aG nuevogrupo nuevouser`.
   - Permisos: `chmod` cambia permisos (r=4, w=2, x=1; ej. 755 = rwxr-xr-x).
     - `touch archivo; chmod 644 archivo`: Lectura/escritura para dueño, lectura para otros.
   - Dueño: `chown nuevouser:nuevogrupo archivo`.
   - Nota para macOS: `/etc/passwd` puede variar; usa ejemplos adaptados.

2. **Procesos/Señales**:
   - `ps aux`: Lista todos los procesos.
   - `top`: Monitor interactivo (presiona q para salir).
   - Señales: `kill -SIGTERM PID` (termina proceso; encuentra PID con `ps`).
     - `kill -9 PID`: Fuerza terminación (SIGKILL).

3. **systemd**:
   - `systemctl status`: Muestra estado de un servicio (ej. `systemctl status ssh`).
   - Iniciar/parar: `sudo systemctl start/stop servicio`.
   - Habilitar al boot: `sudo systemctl enable servicio`.
   - Nota para macOS: No hay systemd; usa análogos como `launchctl` o `brew services` (si tienes Homebrew instalado).

4. **journalctl**:
   - `journalctl -u servicio`: Logs de un servicio.
   - `journalctl -f`: Sigue logs en tiempo real.
   - `journalctl --since "2025-08-29"`: Logs desde una fecha.
   - Compatibilidad: En WSL2 sin systemd (verifica con `systemctl`), fallback: `sudo tail -n 100 /var/log/syslog` o como última opción `sudo dmesg --ctime | tail -n 50`.
     En macOS: `log show --last 1h | grep -i error` o `tail -f /var/log/system.log`.

**Indicación para WSL2/Windows**: En WSL2, systemd no está habilitado por defecto en versiones antiguas; actualiza con `sudo apt update && sudo apt upgrade`. 
Para habilitar systemd: Edita `/etc/wsl.conf` con `sudo nano /etc/wsl.conf` y agrega `[boot]\nsystemd=true`, luego reinicia WSL con `wsl --shutdown` desde PowerShell.

#### Ejercicios de reforzamiento
1. Crea un usuario "devsec" y agrégalo a un grupo "ops". Cambia permisos de un archivo para que solo "devsec" lo lea: `sudo adduser devsec; sudo addgroup ops; sudo usermod -aG ops devsec; touch secreto.txt; sudo chown devsec:ops secreto.txt; sudo chmod 640 secreto.txt` (usa mock si es entorno compartido).

    ![](imagenes/sesion2_1_1.png)

    ![](imagenes/sesion2_1_2.png)

    ![](imagenes/sesion2_1_3.png)


2. Lista procesos, encuentra el PID de tu shell (`ps aux | grep bash`), y envía una señal SIGTERM (no lo mates si es crítico).

    ![](imagenes/sesion2_2.png)

3. Verifica el estado de un servicio como "systemd-logind" con `systemctl status systemd-logind`

    ![](imagenes/sesion2_3_1.png)


    Y ve sus logs con `journalctl -u systemd-logind -n 10`.

    ![](imagenes/sesion2_3_2.png)

4. (Intermedio) Inicia un proceso en background (`sleep 100 &`), lista con `ps`, y mátalo con `kill`.

    ![](imagenes/sesion2_4.png)
  

#### Comprobación
- `namei -l secreto.txt` (verifica permisos y propietario).

    ![](imagenes/comprobacion2_1.png)

- `id devsec` (confirma grupos).

    ![](imagenes/comprobacion2_2.png)

### Sección 3: Utilidades de texto de Unix
#### Riesgo & Mitigación en DevSecOps
Riesgo: Procesamiento de logs puede exponer datos sensibles o causar borrados masivos. 
Mitigación: Usa filtros como `journalctl -p err..alert` para severidades, rotación de logs, y opciones seguras en find/xargs (-i para interactivo, -- para seguridad).

#### Marco teórico
El "Utilidades de texto Unix" es un conjunto de herramientas para procesar texto, vital en DevSecOps para analizar logs, parsear outputs de herramientas de seguridad (como Nmap o OWASP ZAP), y automatizar informes. 
- **grep**: Busca patrones en texto.
- **sed**: Edita streams de texto (sustituir, eliminar).
- **awk**: Procesa datos estructurados (columnas).
- **cut**: Extrae campos.
- **sort/uniq**: Ordena y elimina duplicados.
- **tr**: Traduce caracteres.
- **tee**: Divide salida a múltiples destinos.
- **find**: Busca archivos por criterios.

Estas herramientas permiten pipelines eficientes para tareas como filtrado de vulnerabilidades en scans.

#### Explicaciones paso a paso
1. **grep**: `grep patrón archivo` (ej. `grep error /var/log/syslog`).
   - Opciones: `-i` (insensible mayúsculas), `-r` (recursivo).

2. **sed**: `sed 's/viejo/nuevo/' archivo` (sustituye).
   - `sed '/patrón/d' archivo`: Elimina líneas.

3. **awk**: `awk '{print $1}' archivo` (imprime primera columna).
   - Separador: `awk -F: '{print $1}' /etc/passwd`.

4. **cut**: `cut -d: -f1 /etc/passwd` (primera columna separada por :).

5. **sort/uniq**: `sort archivo | uniq` (ordena y quita duplicados).

6. **tr**: `tr 'a-z' 'A-Z' < archivo` (convierte a mayúsculas).

7. **tee**: `comando | tee archivo` (muestra y guarda).

8. **find**: `find /directorio -name "*.txt"` (busca archivos).

Crea un archivo de prueba: `printf "linea1: dato1\nlinea2: dato2\n" > datos.txt`.

#### Ejercicios de reforzamiento
1. Usa grep para buscar "root" en `/etc/passwd`: `grep root /etc/passwd`.

    ![](imagenes/sesion3_1.png)

2. Con sed, sustituye "dato1" por "secreto" en datos.txt: `sed 's/dato1/secreto/' datos.txt > nuevo.txt`.
  
    ![](imagenes/sesion3_2.png)

3. Con awk y cut, extrae usuarios de `/etc/passwd`: `awk -F: '{print $1}' /etc/passwd | sort | uniq`.

    ![](imagenes/sesion3_3.png)

4. Usa tr para convertir un texto a mayúsculas y tee para guardarlo: `printf "hola\n" | tr 'a-z' 'A-Z' | tee mayus.txt`.

    ![](imagenes/sesion3_4.png)

5. (Intermedio) Encuentra archivos en `/tmp` modificados en los últimos 5 días: `find /tmp -mtime -5 -type f`.

    ![](imagenes/sesion3_5.png)

6. Pipeline completo: `ls /etc | grep conf | sort | tee lista_conf.txt | wc -l`.

    ![](imagenes/sesion3_6.png)

7. (Opcional) Usa tee para auditoría: `grep -Ei 'error|fail' evidencias/sesion.txt | tee evidencias/ hallazgos.txt`.

    ![](imagenes/sesion3_7.png)

#### Comprobación
- `file lista_conf.txt && head lista_conf.txt` (verifica tipo y contenido).

  ![](imagenes/comprobacion3_1.png)

- `cat mayus.txt` (confirma transformación).

  ![](imagenes/comprobacion3_2.png)