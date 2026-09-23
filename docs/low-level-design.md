# Low-level design
`LifeEvent` holds normalized event identity and a flexible attributes map. `Workflow` owns `WorkflowTask` instances, whose transition table prevents invalid lifecycle changes. `WorkflowPlanner` maps extensible event types to independent rules. Repository, AI, and government contracts in `ports.py` enforce dependency inversion; `MemoryStore`, `MockConversationAI`, and `MockGovernmentProvider` are replaceable adapters.

Important operations write `AuditEvent`s. Confirmation is required before provider submission. Idempotency uses a resident/type/date fingerprint, with the repository as the persistence enforcement point; a production SQL implementation should enforce a unique index on these fields.
