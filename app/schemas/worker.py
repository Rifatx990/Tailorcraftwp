from pydantic import BaseModel

# ----------------------------
# Worker Schemas
# ----------------------------
class WorkerBase(BaseModel):
    name: str
    phone: str
    role: str
    salary_type: str

class WorkerCreate(WorkerBase):
    password: str

class WorkerResponse(WorkerBase):
    id: int

    class Config:
        orm_mode = True

class WorkerTaskSchema(BaseModel):
    worker_id: int
    order_id: int
    status: str = "Pending"
