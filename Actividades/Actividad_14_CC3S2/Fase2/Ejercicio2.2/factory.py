from typing import Dict, Any
import uuid
from datetime import datetime
from iac_patterns.factory import NullResourceFactory

class TimestampedNullResourceFactory(NullResourceFactory):
    @staticmethod
    def create(name: str, fmt: str) -> Dict[str, Any]:
        ts = datetime.utcnow().strftime(fmt)
        triggers = {
            "factory_uuid": str(uuid.uuid4()),
            "timestamp": ts
        }
        return super(TimestampedNullResourceFactory, TimestampedNullResourceFactory).create(name, triggers)
