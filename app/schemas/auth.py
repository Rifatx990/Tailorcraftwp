from pydantic import BaseModel, EmailStr

# ----------------------------
# Auth Schemas
# ----------------------------
class LoginSchema(BaseModel):
    username: str
    password: str

class TokenSchema(BaseModel):
    access_token: str
    token_type: str

class CustomerRegisterSchema(BaseModel):
    name: str
    email: EmailStr
    phone: str
    password: str

class WorkerCreateSchema(BaseModel):
    name: str
    phone: str
    role: str
    salary_type: str
    password: str
