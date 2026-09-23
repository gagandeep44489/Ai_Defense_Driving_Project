from datetime import date
import pytest
from uae_navigator.application import LifeEventService, WorkflowPlanner
from uae_navigator.domain import DuplicateLifeEvent, InvalidTaskTransition, TaskStatus
from uae_navigator.infrastructure import MemoryStore, MockConversationAI, MockGovernmentProvider

def build(fail=False):
 s=MemoryStore(); return LifeEventService(s,s,s,MockConversationAI(),WorkflowPlanner(),MockGovernmentProvider(fail)),s
def test_birth_creates_four_task_workflow():
 svc,_=build(); e=svc.report("resident-1","My wife and I had a baby.",date(2026,1,1)); w=svc.analyze(e.id)
 assert len(w.tasks)==4 and w.tasks[0].title=="Birth registration"
def test_marriage_creates_workflow():
 svc,_=build(); e=svc.report("resident-1","We got married",date(2026,1,1)); assert len(svc.analyze(e.id).tasks)==2
def test_duplicate_is_rejected_and_no_second_workflow():
 svc,_=build(); e=svc.report("r","baby born",date(2026,1,1)); svc.analyze(e.id)
 with pytest.raises(DuplicateLifeEvent): svc.report("r","baby born again",date(2026,1,1))
def test_invalid_transition_rejected():
 svc,_=build(); task=svc.analyze(svc.report("r","baby",date(2026,1,1)).id).tasks[0]
 with pytest.raises(InvalidTaskTransition): task.transition(TaskStatus.COMPLETED)
def test_confirmation_and_mock_failure():
 svc,_=build(True); w=svc.analyze(svc.report("r","baby",date(2026,1,1)).id)
 with pytest.raises(ValueError): svc.submit(w.id)
 svc.confirm(w.id); svc.submit(w.id); assert all(t.status==TaskStatus.FAILED for t in w.tasks)
def test_workflow_aggregates_completed_tasks():
 svc,_=build(); w=svc.analyze(svc.report("r","baby",date(2026,1,1)).id)
 for task in w.tasks:
  task.transition(TaskStatus.READY); task.transition(TaskStatus.IN_PROGRESS); task.transition(TaskStatus.COMPLETED)
 assert w.status == TaskStatus.COMPLETED

def test_list_tasks_returns_task_dtos_for_an_existing_workflow():
 pytest.importorskip("fastapi")
 from uae_navigator import api
 event=api.service.report("api-resident","baby born",date(2026,1,1))
 workflow=api.service.analyze(event.id)

 assert api.list_tasks(workflow.id) == api.workflow_dto(workflow)["tasks"]
