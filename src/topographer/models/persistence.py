from __future__ import annotations

"""Data models for persistence pairing results."""

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class PersistencePair:
    """Single birth/death persistence pair.

    Attributes
    ----------
    birth, death:
        Paired critical entities (usually node identifiers).
    birth_scalar, death_scalar:
        Scalar values at birth and death.
    persistence:
        Absolute difference between death and birth scalar values.
    """

    birth: Any
    death: Any
    birth_scalar: float
    death_scalar: float
    persistence: float

    def to_dict(self) -> dict[str, Any]:
        """Serialize the pair to a JSON-friendly dictionary."""
        return asdict(self)


@dataclass(slots=True)
class PersistenceResult:
    """Collection of persistence pairs computed for one scalar field."""

    scalar: str
    pairs: list[PersistencePair] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the result payload to a JSON-friendly dictionary."""
        return {
            "scalar": self.scalar,
            "pairs": [pair.to_dict() for pair in self.pairs],
        }


__all__ = ["PersistencePair", "PersistenceResult"]
