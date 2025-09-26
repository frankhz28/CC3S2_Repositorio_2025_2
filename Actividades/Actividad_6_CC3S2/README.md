# **Actividad 6**: Introducción a Git conceptos básicos y operaciones esenciales

## Comandos Git utilizados

`git log --graph --pretty=format:'%x09 %h %ar ("%an") %s'`

Nos muestra el historial de commits en un formato grafico con informacion personalizada de acuerdo a sus componentes.

**Componentes del formato**:
- `%x09`: Agrega una tabulacion para mejorar la alineacion
- `%h`: Hash corto del commit (7 caracteres)
- `%ar`: Fecha relativa
- `%an`: Nombre del autor
- `%s`: Mensaje del commit

    **Salida obtenida**:
    ```
    * 	 b025d36 7 hours ago ("frankhz28") Main cherry-pick
    * 	 82c5c21 6 hours ago ("frankhz28") Agrega ejemplo de cherry-pick
    *   	 f10ea3b 7 hours ago ("frankhz28") Conflicto solucionado
    |\  
    | * 	 3343bd7 7 hours ago ("frankhz28") Corregir error en la funcionalidad de rollback
    * | 	 82f5570 7 hours ago ("frankhz28") Main revert HEAD squash
    [...]
    ```

## Respuestas a las Preguntas

### ¿Cómo te ha ayudado Git a mantener un historial claro y organizado de tus cambios?

Gracias a su orden cronologico e identifiacion unica **Git** permite darle un mejor seguimiento a la evolucion del proyecto asi como tener referenciado los cambios para un mejor desplazamiento entre lineas temporales.

### ¿Qué beneficios ves en el uso de ramas para desarrollar nuevas características o corregir errores?

Trabajar con ramas tiene muchos beneficios, como :
- **Desarrollo paralelo**, podemos desarrollar multiples características simultaneamente sin interferencias
- **Aislamiento de cambios**, nuestros experimentos y nuevas características no afectan la rama principal
- **Facilita colaboración**, permite a diferentes desarrolladores trabajar en ramas separadas
- **Rollback seguro**, si una característica falla podemos descartar la rama sin afectar el codigo principal

### Revisión final del historial de commits

**Comando utilizado**: `git log --oneline --graph --all`


```
* b025d36 Main cherry-pick
* 82c5c21 Agrega ejemplo de cherry-pick
*   f10ea3b Conflicto solucionado
|\  
| * 3343bd7 Corregir error en la funcionalidad de rollback
* | 82f5570 Main revert HEAD squash
* | b4bb981 Revert "Main modificado"
* | d2168b2 Main modificado
* |   043b1f5 Resuelve el conflicto de fusión entre la versión main y feature/advanced-feature
|\ \  
| * | ade2fad Agrega la funcion greet como función avanzada
| |/  
* / 201be01 Actualizar el mensaje main.py en la rama main
|/  
* 8a610b0 Actualizar el mensaje main.py en la rama main
* e6a7189 Agrega main.py
* 0695eab Configura la documentación base del repositorio
* 12567f5 Commit inicial con README.md
```

### Revisión de ramas y merges

**Comando utilizado**: `git branch -vv`

```
  develop                     e6a7189 Agrega main.py
  feature/another-new-feature 0695eab Configura la documentación base del repositorio
* feature/cherry-pick         b025d36 Main cherry-pick
  feature/login               e6a7189 Agrega main.py
  feature/new-feature         e6a7189 Agrega main.py
  hotfix/bugfix               0695eab Configura la documentación base del repositorio
  main                        82c5c21 Agrega ejemplo de cherry-pick

```  

## Tabla Resumen de Comandos Git Utilizados

| Comando | Propósito | Archivo de salida | Descripción |
|---------|-----------|-------------------|-------------|
| `git --version` | Verificar versión de Git | `logs/git-version.txt` | Muestra la versión instalada de Git |
| `git config --list` | Listar configuración | `logs/config.txt` | Muestra toda la configuración de Git (global/local) |
| `git config --global user.name "frankhz28"` | Configurar usuario | - | Establece el nombre del usuario globalmente |
| `git config --global user.email "usuario@example.com"` | Configurar email | - | Establece el email del usuario globalmente |
| `git init` | Inicializar repositorio | `logs/init-status.txt` | Crea un nuevo repositorio Git |
| `git status` | Estado del repositorio | `logs/init-status.txt` | Muestra el estado actual de archivos |
| `git add .` | Agregar archivos | `logs/add-commit.txt` | Agrega todos los archivos al staging area |
| `git add main.py` | Agregar archivo específico | `logs/add-commit.txt` | Agrega un archivo específico al staging area |
| `git commit -m "mensaje"` | Confirmar cambios | `logs/add-commit.txt` | Crea un commit con los cambios preparados |
| `git log --oneline` | Historial compacto | `logs/log-oneline.txt` | Muestra el historial en una línea por commit |
| `git log --graph --all` | Historial gráfico | - | Visualiza el historial con ramas y merges |
| `git log --author="frankhz28"` | Filtrar por autor | - | Muestra commits de un autor específico |
| `git branch` | Listar ramas | - | Muestra todas las ramas locales |
| `git branch -vv` | Ramas detalladas | `logs/branches.txt` | Muestra ramas con información adicional |
| `git branch feature/nueva-rama` | Crear rama | - | Crea una nueva rama desde la actual |
| `git checkout rama` | Cambiar rama | - | Cambia a una rama específica |
| `git checkout -b nueva-rama` | Crear y cambiar | - | Crea una nueva rama y cambia a ella |
| `git switch rama` | Cambiar rama (nuevo) | - | Forma moderna de cambiar entre ramas |
| `git merge rama` | Fusionar ramas | `logs/merge-o-conflicto.txt` | Fusiona una rama en la actual |
| `git branch -d rama` | Eliminar rama | - | Elimina una rama local fusionada |
| `git revert HEAD` | Revertir commit | `logs/revert.txt` | Crea un commit que deshace cambios anteriores |
| `git reset --hard HEAD~1` | Resetear historial | - | Elimina commits del historial (peligroso) |
| `git restore archivo` | Restaurar archivo | - | Deshace cambios no confirmados en un archivo |
| `git cherry-pick hash` | Aplicar commit específico | `logs/cherry-pick.txt` | Aplica un commit específico a la rama actual |
| `git stash` | Guardar cambios temporalmente | `logs/stash.txt` | Guarda cambios sin confirmar temporalmente |
| `git stash pop` | Recuperar cambios | `logs/stash.txt` | Aplica los cambios guardados en stash |
| `git rebase -i HEAD~3` | Rebase interactivo | `logs/rebase.txt` | Reorganiza/combina commits interactivamente |



