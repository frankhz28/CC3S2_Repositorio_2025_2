from typing import Dict, Any
import os
import json
from iac_patterns.factory import NullResourceFactory
from iac_patterns.composite import CompositeModule
from iac_patterns.prototype import ResourcePrototype

class InfrastructureBuilder:
    def __init__(self, env_name: str) -> None:
        self.env_name = env_name
        self._module = CompositeModule()

    def build_null_fleet(self, count: int = 5) -> "InfrastructureBuilder":
        base_proto = ResourcePrototype(
            NullResourceFactory.create("placeholder")
        )
        for i in range(count):
            def mutator(d: Dict[str, Any], idx=i) -> None:
                res_block = d["resource"][0]["null_resource"][0]
                original_name = next(iter(res_block.keys()))
                new_name = f"{original_name}_{idx}"
                res_block[new_name] = res_block.pop(original_name)
                res_block[new_name][0]["triggers"]["index"] = idx
            clone = base_proto.clone(mutator).data
            self._module.add(clone)
        return self

    def build_group(self, name: str, size: int) -> "InfrastructureBuilder":
        base = NullResourceFactory.create(name)
        proto = ResourcePrototype(base)
        group = CompositeModule()
        for i in range(size):
            def mut(block, idx=i):
                res = block["resource"][0]["null_resource"][0].pop(name)
                block["resource"][0]["null_resource"][0][f"{name}_{idx}"] = res
            group.add(proto.clone(mut).data)
        self._module.add({"module": {name: group.export()}})
        return self

    def export(self, path: str) -> None:
        data = self._module.export()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
        print(f"[Builder] Terraform JSON escrito en: {path}")
