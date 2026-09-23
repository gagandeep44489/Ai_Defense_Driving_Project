# Domain model
Life events include resident, type, date, confidence, and extracted attributes. A workflow is created from one event. Tasks contain service, documents, priority, external reference, and a state. Valid transitions are PENDING→READY/BLOCKED/CANCELLED, READY→IN_PROGRESS/BLOCKED/CANCELLED, IN_PROGRESS→COMPLETED/FAILED/BLOCKED, BLOCKED→READY/CANCELLED, and FAILED→READY/CANCELLED.
