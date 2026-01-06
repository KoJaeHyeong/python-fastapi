from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

DATABASE_URL = "mysql+pymysql://ko1586:1234@127.0.0.1:3306/todos"

engine = create_engine(
    DATABASE_URL,
)  # echo=True: 모든 SQL 쿼리를 콘솔에 출력

SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()
        print("DB Pool closed@!!")
