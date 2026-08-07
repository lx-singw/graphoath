# GraphOath — Module SDK & Open-Source Contributor Handbook

This document provides the developer handbook for building new GraphOath modules and contributing open-source extensions using the **GraphOath Module SDK**.

---

## 1. Module Architecture Contract

Every GraphOath module inherits from `BaseGraphOathModule` and implements four pure interfaces:

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BaseGraphOathModule(ABC):
    
    @abstractmethod
    def ingest_trigger(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Stage 1: Normalize inbound MetadataChangeLog event."""
        pass
        
    @abstractmethod
    def gather_evidence(self, event: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Stage 2: Query DataHub MCP / Context Kit for evidence graph."""
        pass
        
    @abstractmethod
    def evaluate_gate(self, claim: str, evidence: List[Dict[str, Any]]) -> bool:
        """Stage 3: Zero-network citation gate evaluation."""
        pass
        
    @abstractmethod
    def execute_action(self, claim: str, evidence: List[Dict[str, Any]]) -> str:
        """Stage 4: Execute native DataHub mutation and write Custody receipt."""
        pass
```

---

## 2. Creating a Custom Module in 3 Steps

1. Create a new directory under `src/graphoath/modules/my_module/`.
2. Implement `pipeline.py` extending `BaseGraphOathModule`.
3. Register the module in `config/default.yaml` under `active_modules`.
