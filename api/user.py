from typing import cast

from cache import redis_client
from database.orm import User
from database.repository import UserRepository
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from schema.request import (CreateOTPRequest, LoginRequest, SignUpRequest,
                            VerifyOTPRequest)
from schema.response import JWTResponse, UserSchema
from security import get_access_token
from service.user import UserService

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/sign-up", status_code=201)
def sign_up(
            req: SignUpRequest,
            user_service: UserService = Depends(),
            user_repository: UserRepository = Depends()
            ) -> UserSchema:
    hashed_password = user_service.hash_password(password=req.password)

    user: User = User.create(username=req.username, hashed_password=hashed_password)

    created_user: User = user_repository.create_user(user=user)

    return UserSchema.from_orm(created_user)


@router.post("/login", status_code=200)
def login(req: LoginRequest, user_repo: UserRepository = Depends(), user_service: UserService = Depends()) -> JWTResponse:

    user : User | None = user_repo.get_user_by_username(username=req.username)

    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")

    verify_password: bool = user_service.verify_password(password=req.password, hashed_password=str(user.password))

    if not verify_password:
        raise HTTPException(status_code=401, detail="Not Authorized")

    access_token: str = user_service.create_jwt(username=req.username)

    return JWTResponse(access_token=access_token)


@router.post("/email/otp")
def create_otp(
    req: CreateOTPRequest,
    _: str = Depends(get_access_token), # 변수를 사용할것은 아니기 때문
    user_service: UserService = Depends()
):
    otp: int = user_service.create_otp()
    redis_client.set(req.email, otp)
    redis_client.expire(req.email, 3 * 60)

    return {"otp": otp}

# git 올리기 용
@router.post('/email/otp/verify')
def verify_otp(
    req: VerifyOTPRequest,
    background_tasks: BackgroundTasks,
    access_token: str = Depends(get_access_token),
    user_service: UserService = Depends(),
    user_repo: UserRepository = Depends()
) -> UserSchema:
    otp: str | None = cast(str, redis_client.get(req.email))

    if not otp:
        raise HTTPException(status_code=400, detail="Bad Request")

    if req.otp != int(otp):
        raise HTTPException(status_code=400, detail="Diff OTP")

    username: str = user_service.verify_jwt(access_token=access_token)

    user: User | None = user_repo.get_user_by_username(username=username)

    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")

    user_repo.create_user_email(email=req.email, id=cast(int, user.id))

    background_tasks.add_task(
        user_service.send_email,
        email = req.email
    )


    return UserSchema.from_orm(user)

