import os
import json
import re

LEGACY_DIR = "legacy"
OUTPUT_DIR = "migrated_env"

def parse_config_file(filepath):
    """Lee el .cfg y lo convierte en un dict {'PORT': '8080'}."""
    config = {}
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            # Divide la línea en clave/valor en el primer '='
            if '=' in line:
                key, value = line.split('=', 1)
                config[key] = value
    print(f"Config leída: {config}")
    return config

def parse_script_file(filepath):
    """Lee el .sh y extrae los comandos ejecutables."""
    commands = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            # Ignora el shebang y líneas vacías/comentarios
            if not line or line.startswith('#!'):
                continue
            commands.append(line)
    
    # Para este lab, unimos todos los comandos en uno solo
    command_str = " && ".join(commands)
    print(f"Comando leído: {command_str}")
    return command_str

def translate_to_terraform(config, script_command):
    """
    Traduce las variables de config y script a sintaxis de Terraform.
    """
    tf_variables = {}
    tf_main = {}
    
    # 1. Traducir el comando (ej. $PORT -> ${var.port})
    # Asumimos que la config_key (PORT) se usa como $PORT en el script
    tf_command = script_command
    for key in config:
        # por convención de terraform, usamos minúsculas
        tf_var_name = key.lower() 
        # Reemplaza $KEY (Bash) por ${var.key} (Terraform)
        tf_command = tf_command.replace(f'${key}', f'${{var.{tf_var_name}}}')

    print(f"Comando traducido a TF: {tf_command}")
    
    # 2. Generar el network.tf.json (Definición de Variables)
    tf_vars_list = []
    for key, value in config.items():
        tf_var_name = key.lower()
        tf_vars_list.append({
            tf_var_name: [{
                "type": "string",
                "default": value,
                "description": f"Variable migrada desde legacy/config.cfg"
            }]
        })
    tf_variables = {"variable": tf_vars_list}

    # 3. Generar el main.tf.json (El Recurso)
    tf_main = {
        "resource": [{
            "null_resource": [{
                "legacy_server": [{ # Usamos un nombre de recurso descriptivo
                    "triggers": { 
                        # El trigger vigila el valor de la variable
                        tf_var_name: f"${{var.{tf_var_name}}}"
                    },
                    "provisioner": [{
                        "local-exec": {
                            "command": tf_command
                        }
                    }]
                }]
            }]
        }]
    }
    
    return tf_variables, tf_main

def write_files(out_dir, network_tf, main_tf):
    """Escribe los archivos JSON generados en el directorio de salida."""
    os.makedirs(out_dir, exist_ok=True)
    
    network_path = os.path.join(out_dir, "network.tf.json")
    main_path = os.path.join(out_dir, "main.tf.json")
    
    with open(network_path, "w") as f:
        json.dump(network_tf, f, indent=4, sort_keys=True)
        
    with open(main_path, "w") as f:
        json.dump(main_tf, f, indent=4, sort_keys=True)
        
    print(f"Archivos de Terraform generados en '{out_dir}/'")

if __name__ == "__main__":
    config_path = os.path.join(LEGACY_DIR, "config.cfg")
    script_path = os.path.join(LEGACY_DIR, "run.sh")
    
    config_data = parse_config_file(config_path)
    script_command = parse_script_file(script_path)
    
    tf_vars, tf_main = translate_to_terraform(config_data, script_command)
    
    write_files(OUTPUT_DIR, tf_vars, tf_main)