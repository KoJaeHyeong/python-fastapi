from redis import Redis

redis_client: Redis = Redis(
    host="localhost",
    port=6379,
    db=0,
    encoding="utf-8",
    decode_responses=True,  # 반환 시 python 데이터 타입으로 변환 (저장될 시 bytes타입으로 저장되어 있기 때문)
)
