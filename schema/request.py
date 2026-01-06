from pydantic import BaseModel


class CreateTodoRequest(
    BaseModel
):  # pydantic의 BaseModel이 타입검사 등 request body로 이용하게 해줌
    contents: str
    is_done: bool

class SignUpRequest(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class CreateOTPRequest(BaseModel):
    email: str

class VerifyOTPRequest(BaseModel):
    email: str
    otp: int
