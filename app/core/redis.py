import redis

redis_client = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True,
)

def revoke_token(jti: str, expires_in: int):
    redis_client.setex(
        f"revoked:{jti}",
        expires_in,
        "true"
    )



def is_token_revoked(jti: str) -> bool:
    return redis_client.exists(f"revoked:{jti}") == 1
