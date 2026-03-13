from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class PersistencePair:
    birth: Any
    death: Any
    birth_scalar: float
    death_scalar: float
    persistence: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class PersistenceResult:
    scalar: str
    pairs: list[PersistencePair] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "scalar": self.scalar,
            "pairs": [pair.to_dict() for pair in self.pairs],
        }


__all__ = ["PersistencePair", "PersistenceResult"]
