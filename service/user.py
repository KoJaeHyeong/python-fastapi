import random
import time
from datetime import datetime, timedelta

import bcrypt
from fastapi import HTTPException
from jose import jwt
from jose.constants import ALGORITHMS


class UserService:
    encoding = "utf-8"
    secret_key = "26cc5caca645f037a9b906b118fc97f8a9c0db316c6565a85f7136b6c8da7d70"
    jwt_algorithm = ALGORITHMS.HS256

    def hash_password(self, password: str) -> str:
        hashed_password: bytes = bcrypt.hashpw(
            password=password.encode(self.encoding), salt=bcrypt.gensalt()
        )

        return hashed_password.decode(self.encoding)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        try:
            return bcrypt.checkpw(
                password=password.encode(self.encoding),
                hashed_password=hashed_password.encode(self.encoding),
            )

        except Exception as e:
            print(e)
            return False

    def create_jwt(self, username: str) -> str:
        return jwt.encode(
            claims={"sub": username, "exp": datetime.now() + timedelta(minutes=2)},
            key=self.secret_key,
            algorithm=self.jwt_algorithm,
        )

    def verify_jwt(self, access_token: str) -> str:
        try:
            payload: dict = jwt.decode(
                token=access_token, key=self.secret_key, algorithms=[self.jwt_algorithm]
            )

            print("====================")
            print(payload)
            print("====================")

            return payload["sub"]
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid token")

    @staticmethod  # 인스턴스 속성에 접근할 필요없기 때문에 static처리
    def create_otp() -> int:
        return random.randint(1000, 9999)

    @staticmethod
    def send_email(email: str) -> None:
        time.sleep(10)
        print(f"Sending email to {email}")
