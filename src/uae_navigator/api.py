from datetime import date
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from .infrastructure import MemoryStore,MockConversationAI,MockGovernmentProvider
from .application import LifeEventService,WorkflowPlanner
from .domain import *
store=MemoryStore(); service=LifeEventService(store,store,store,MockConversationAI(),WorkflowPlanner(),MockGovernmentProvider())
app=FastAPI(title="UAE LifeEvent Voice Navigator",version="0.1.0")
class Report(BaseModel): resident_id:str=Field(min_length=1); text:str=Field(min_length=3); event_date:date|None=None
class TaskUpdate(BaseModel): status:TaskStatus
@app.exception_handler(ValueError)
async def app_error(_:Request,e:ValueError): return JSONResponse(status_code=409 if isinstance(e,DuplicateLifeEvent) else 422,content={"error":type(e).__name__,"detail":str(e)})
@app.exception_handler(NotFound)
async def not_found(_:Request,e:NotFound): return JSONResponse(status_code=404,content={"error":"not_found","detail":str(e)})
@app.get("/api/v1/health")
def health(): return {"status":"ok","providers":{"government":"mock","conversation_ai":"mock"}}
@app.post("/api/v1/life-events")
def report(body:Report):
 e=service.report(body.resident_id,body.text,body.event_date); return {"id":e.id,"event_type":e.event_type,"confidence":e.confidence,"message":"Event saved; nothing has been submitted."}
@app.get("/api/v1/life-events/{event_id}")
def get_event(event_id:str):
 e=store.events.get(event_id)
 if not e: raise NotFound("Life event not found")
 return {"id":e.id,"resident_id":e.resident_id,"event_type":e.event_type,"event_date":e.event_date,"attributes":e.attributes,"status":e.status}
@app.post("/api/v1/voice/command")
def voice_command(body:Report): return report(body)
@app.post("/api/v1/voice/transcribe")
def transcribe(body:Report): return {"text":body.text,"provider":"mock","warning":"No audio processing occurs in the MVP."}
@app.post("/api/v1/life-events/{event_id}/analyze")
def analyze(event_id:str):
 w=service.analyze(event_id); return workflow_dto(w)
@app.post("/api/v1/workflows/{workflow_id}/confirm")
def confirm(workflow_id:str): return workflow_dto(service.confirm(workflow_id))
@app.post("/api/v1/workflows/{workflow_id}/submit")
def submit(workflow_id:str): return workflow_dto(service.submit(workflow_id))
@app.get("/api/v1/workflows/{workflow_id}")
def get_workflow(workflow_id:str):
 w=store.get(workflow_id)
 if not w: raise NotFound("Workflow not found")
 return workflow_dto(w)
@app.get("/api/v1/workflows/{workflow_id}/tasks")
def list_tasks(workflow_id:str): return get_workflow(workflow_id)["tasks"]
@app.get("/api/v1/life-events/{event_id}/notifications")
def notifications(event_id:str):
 if not store.events.get(event_id): raise NotFound("Life event not found")
 return []
@app.post("/api/v1/tasks/{task_id}/status")
def update_task(task_id:str,body:TaskUpdate):
 task=next((t for w in store.workflows.values() for t in w.tasks if t.id==task_id),None)
 if not task: raise NotFound("Task not found")
 task.transition(body.status); store.record(AuditEvent("task_status_changed","task",task.id)); return {"id":task.id,"status":task.status}
def workflow_dto(w): return {"id":w.id,"life_event_id":w.life_event_id,"status":w.status,"confirmed":w.confirmed,"tasks":[{"id":t.id,"title":t.title,"status":t.status,"required_documents":t.required_documents,"external_reference_id":t.external_reference_id} for t in w.tasks]}
