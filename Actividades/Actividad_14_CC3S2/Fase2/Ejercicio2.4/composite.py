from typing import List, Dict, Any

class CompositeModule:
    def __init__(self) -> None:
        self._children: List[Dict[str, Any]] = []

    def add(self, resource_dict: Dict[str, Any]) -> None:
        self._children.append(resource_dict)

    def export(self) -> Dict[str, Any]:
        merged: Dict[str, Any] = {"module": {}, "resource": []}
        for child in self._children:
            if "module" in child:
                merged["module"].update(child["module"])
            if "resource" in child:
                merged["resource"].extend(child["resource"])
        return merged

# Ejemplo de uso para submódulos
if __name__ == "__main__":
    network = {"module": {"network": {"resource": [{"null_resource": [{"net": [ {"triggers": {"x": 1}} ]}] }]}}}
    app = {"module": {"app": {"resource": [{"null_resource": [{"app": [ {"triggers": {"y": 2}} ]}] }]}}}
    comp = CompositeModule()
    comp.add(network)
    comp.add(app)
    import json
    print(json.dumps(comp.export(), indent=2))
