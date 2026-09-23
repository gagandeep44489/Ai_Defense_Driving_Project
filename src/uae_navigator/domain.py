from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from enum import Enum
from uuid import uuid4

def now() -> datetime: return datetime.now(timezone.utc)

class LifeEventType(str, Enum): BIRTH="BIRTH"; MARRIAGE="MARRIAGE"; DEATH="DEATH"; RELOCATION="RELOCATION"; NAME_CHANGE="NAME_CHANGE"; OTHER="OTHER"
class TaskStatus(str, Enum): PENDING="PENDING"; READY="READY"; IN_PROGRESS="IN_PROGRESS"; BLOCKED="BLOCKED"; COMPLETED="COMPLETED"; FAILED="FAILED"; CANCELLED="CANCELLED"
class EventStatus(str, Enum): DRAFT="DRAFT"; ANALYZED="ANALYZED"; CONFIRMED="CONFIRMED"

class InvalidTaskTransition(ValueError): pass
class DuplicateLifeEvent(ValueError): pass
class NotFound(ValueError): pass

TRANSITIONS = {TaskStatus.PENDING:{TaskStatus.READY,TaskStatus.BLOCKED,TaskStatus.CANCELLED}, TaskStatus.READY:{TaskStatus.IN_PROGRESS,TaskStatus.BLOCKED,TaskStatus.CANCELLED}, TaskStatus.IN_PROGRESS:{TaskStatus.COMPLETED,TaskStatus.FAILED,TaskStatus.BLOCKED}, TaskStatus.BLOCKED:{TaskStatus.READY,TaskStatus.CANCELLED}, TaskStatus.FAILED:{TaskStatus.READY,TaskStatus.CANCELLED}, TaskStatus.COMPLETED:set(), TaskStatus.CANCELLED:set()}

@dataclass
class LifeEvent:
    resident_id: str; event_type: LifeEventType; event_date: date; attributes: dict[str,str] = field(default_factory=dict); confidence: float=0.0; id: str=field(default_factory=lambda:str(uuid4())); status: EventStatus=EventStatus.DRAFT; created_at: datetime=field(default_factory=now)
    @property
    def fingerprint(self): return f"{self.resident_id}:{self.event_type.value}:{self.event_date.isoformat()}"
@dataclass
class WorkflowTask:
    title: str; description: str; service_id: str; required_documents: list[str]; priority: int=2; id: str=field(default_factory=lambda:str(uuid4())); status: TaskStatus=TaskStatus.PENDING; external_reference_id: str|None=None
    def transition(self, target: TaskStatus):
        if target not in TRANSITIONS[self.status]: raise InvalidTaskTransition(f"Cannot transition {self.status} to {target}")
        self.status=target
@dataclass
class Workflow:
    life_event_id: str; tasks: list[WorkflowTask]; id: str=field(default_factory=lambda:str(uuid4())); confirmed: bool=False
    @property
    def status(self):
        states={x.status for x in self.tasks}
        if TaskStatus.FAILED in states: return TaskStatus.FAILED
        if states == {TaskStatus.COMPLETED}: return TaskStatus.COMPLETED
        if TaskStatus.IN_PROGRESS in states: return TaskStatus.IN_PROGRESS
        if TaskStatus.BLOCKED in states: return TaskStatus.BLOCKED
        return TaskStatus.READY if TaskStatus.READY in states else TaskStatus.PENDING
@dataclass
class AuditEvent:
    action: str; entity_type: str; entity_id: str; actor: str="system"; metadata: dict[str,str]=field(default_factory=dict); occurred_at: datetime=field(default_factory=now)
