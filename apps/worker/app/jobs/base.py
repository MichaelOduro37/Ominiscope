from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class JobResult:
    status: str
    payload: Dict[str, Any]
