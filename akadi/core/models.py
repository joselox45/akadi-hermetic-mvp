"""Modelos de datos del nucleo AKADI."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Status(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    PARTIAL = "PARTIAL"
    INCONCLUSIVE = "INCONCLUSIVE"
    NOT_RUN = "NOT_RUN"


@dataclass(frozen=True)
class TestCase:
    case_id: str
    objective: str
    input_text: str
    expected_text: str | None = None
    severity: str = "UNASSESSED"
    tags: tuple[str, ...] = ()
    risk_label: str = "UNASSESSED"


@dataclass(frozen=True)
class Evaluation:
    status: Status
    reasons: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.status is Status.PASS and not self.reasons:
            raise ValueError("Un PASS debe remitir a evidencia concreta.")
