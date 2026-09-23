from datetime import date
from .domain import *
class WorkflowPlanner:
 _rules={
  LifeEventType.BIRTH:[("Birth registration","Register the child's birth","birth-registration",["hospital birth notification","parents' Emirates IDs"]),("Emirates ID","Apply for the child's Emirates ID","emirates-id",["birth certificate"]),("Residency","Arrange child residency sponsorship","residency",["passport","birth certificate"]),("Health cover","Review health-insurance enrolment","health-cover",["Emirates ID application reference"])],
  LifeEventType.MARRIAGE:[("Marriage certificate","Register or attest marriage documentation","marriage-registration",["marriage certificate","Emirates IDs"]),("Family residency","Review spouse sponsorship eligibility","residency",["attested marriage certificate","passport"])],
  LifeEventType.RELOCATION:[("Address update","Update registered address","address-update",["tenancy contract","Emirates ID"]) ]}
 def plan(self,event): return Workflow(event.id,[WorkflowTask(a,b,c,d) for a,b,c,d in self._rules.get(event.event_type,[])])
class LifeEventService:
 def __init__(self, events, workflows, audit, ai, planner, government): self.events,self.workflows,self.audit,self.ai,self.planner,self.government=events,workflows,audit,ai,planner,government
 def report(self,resident_id,text,event_date=None):
  result=self.ai.extract(text); event=LifeEvent(resident_id,LifeEventType(result["event_type"]),event_date or date.today(),result["attributes"],result["confidence"]); self.events.add(event); self.audit.record(AuditEvent("life_event_created","life_event",event.id)); return event
 def analyze(self,event_id):
  event=self.events.get(event_id)
  if not event: raise NotFound("Life event not found")
  existing=self.workflows.by_event(event_id)
  if existing:return existing
  event.status=EventStatus.ANALYZED; workflow=self.planner.plan(event); self.workflows.workflows[workflow.id]=workflow; self.audit.record(AuditEvent("workflow_created","workflow",workflow.id)); return workflow
 def confirm(self,workflow_id):
  workflow=self.workflows.get(workflow_id)
  if not workflow: raise NotFound("Workflow not found")
  workflow.confirmed=True; self.audit.record(AuditEvent("confirmation_received","workflow",workflow.id)); return workflow
 def submit(self,workflow_id):
  workflow=self.workflows.get(workflow_id)
  if not workflow: raise NotFound("Workflow not found")
  if not workflow.confirmed: raise ValueError("Resident confirmation is required before mock submission")
  for task in workflow.tasks:
   if task.status in {TaskStatus.PENDING,TaskStatus.READY}:
    task.status=TaskStatus.IN_PROGRESS
    try: task.external_reference_id=self.government.submit(task.service_id,task.id); self.audit.record(AuditEvent("mock_application_submitted","task",task.id))
    except RuntimeError: task.status=TaskStatus.FAILED; self.audit.record(AuditEvent("government_submission_failed","task",task.id))
  return workflow
