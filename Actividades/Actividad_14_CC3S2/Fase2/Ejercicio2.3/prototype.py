from iac_patterns.prototype import ResourcePrototype

# Mutator que añade un bloque local_file y un trigger de bienvenida

def add_welcome_file(block: dict):
    # Asume estructura tipo {"resource": [{"null_resource": [{"app_0": [{"triggers": {...}}]}]}]}
    null_res = block["resource"][0]["null_resource"][0]["app_0"][0]
    null_res["triggers"]["welcome"] = "¡Hola!"
    block["resource"].append({
        "local_file": [{
            "welcome_txt": [{
                "content": "Bienvenido",
                "filename": "${path.module}/bienvenida.txt"
            }]
        }]
    })

# Ejemplo de uso
if __name__ == "__main__":
    base = {
        "resource": [{
            "null_resource": [{
                "app_0": [{
                    "triggers": {"init": True}
                }]
            }]
        }]
    }
    proto = ResourcePrototype(base)
    mutated = proto.clone(add_welcome_file)
    import json
    print(json.dumps(mutated._resource_dict, indent=2, ensure_ascii=False))
