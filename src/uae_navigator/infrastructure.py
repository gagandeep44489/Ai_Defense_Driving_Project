from .domain import LifeEvent, Workflow, AuditEvent
class MemoryStore:
 def __init__(self): self.events={}; self.fingerprints=set(); self.workflows={}; self.audit=[]
 def add(self,event):
  if event.fingerprint in self.fingerprints: from .domain import DuplicateLifeEvent; raise DuplicateLifeEvent("A matching life event already exists")
  self.events[event.id]=event; self.fingerprints.add(event.fingerprint)
 def get(self,id): return self.events.get(id) or self.workflows.get(id)
 def record(self,event): self.audit.append(event)
 def by_event(self,id): return next((w for w in self.workflows.values() if w.life_event_id==id),None)
class MockConversationAI:
 def extract(self,text):
  lower=text.lower()
  if any(x in lower for x in ["baby","born","birth"]): return {"event_type":"BIRTH","confidence":.96,"attributes":{"relationship":"child"}}
  if "marri" in lower or "wedding" in lower: return {"event_type":"MARRIAGE","confidence":.94,"attributes":{}}
  if "move" in lower or "relocat" in lower or "address" in lower: return {"event_type":"RELOCATION","confidence":.9,"attributes":{}}
  return {"event_type":"OTHER","confidence":.4,"attributes":{}}
class MockSpeechToText:
 def transcribe(self,audio): return audio.decode("utf-8")
class MockTextToSpeech:
 def synthesize(self,text): return text.encode("utf-8")
class MockNotificationProvider:
 def __init__(self): self.sent=[]
 def send(self,resident_id,message): self.sent.append((resident_id,message))
class MockGovernmentProvider:
 """Mock only: it never contacts or submits to a UAE government system."""
 def __init__(self, fail=False): self.fail=fail
 def submit(self,service_id,task_id):
  if self.fail: raise RuntimeError("mock provider unavailable")
  return "MOCK-"+task_id[:8]
