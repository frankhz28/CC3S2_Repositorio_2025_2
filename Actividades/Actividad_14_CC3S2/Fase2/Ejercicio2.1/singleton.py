"""Patrón Singleton (modificado para Ejercicio 2.1)

Asegura que una clase tenga una única instancia global, compartida en todo el sistema.
Esta implementación es segura para entornos con múltiples hilos (thread-safe).
"""

import threading
from typing import Any, Dict
from datetime import datetime, timezone

class SingletonMeta(type):
    _instances: Dict[type, "ConfigSingleton"] = {}
    _lock: threading.Lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class ConfigSingleton(metaclass=SingletonMeta):
    def __init__(self, env_name: str = "default") -> None:
        self.env_name = env_name
        self.created_at = datetime.now(tz=timezone.utc).isoformat()
        self.settings: Dict[str, Any] = {}

    def set(self, key: str, value: Any) -> None:
        self.settings[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self.settings.get(key, default)

    def reset(self) -> None:
        """
        Limpia el diccionario de settings pero mantiene el timestamp de creación.
        """
        self.settings.clear()
