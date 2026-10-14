from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.config import settings
from jose import jwt, JWTError
from app.models.user import User
from app.core.database import get_db
from app.core.redis import is_token_revoked
from app.crud.crud_user import get_user
from app.core import exceptions

ALGORITHM = settings.ALGORITHM
EXPIRY_TIME = settings.EXPIRY_TIME

my_token = OAuth2PasswordBearer(tokenUrl="/Auth/api/v1/endpoints/auth/login")

def decode_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise exceptions.AuthenticationException("Invalid authentication credentials")

def get_current_user(db: Session = Depends(get_db), token = Depends(my_token)):
    try:
        payload = decode_token(token=token)
        email: str = payload.get('sub')
        jti: str = payload.get('jti')

        if not jti:
            raise exceptions.AuthenticationException("Invalid jwt id")

        # if is_token_revoked(jti=jti):
        #     raise exceptions.AuthenticationException("Invalid session")
        
        if not email:
            raise exceptions.AuthenticationException("Invalid email credentials")
        
    except JWTError as exc:
        raise exceptions.AuthenticationException("Invalid jwt error credentials")

    user = get_user(db, email=email)
    if not user:
        raise exceptions.AuthenticationException("Invalid authentication credentials")
    return user


allowed_roles = ["SUPER_ADMIN", 
    "MANAGER"
    "CATALOG_MANAGER"
    "SUPPORT"
    "WAREHOUSE"
    "CUSTOMER"
    "VENDOR"
]

def role_checker():
    async def dependency(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise exceptions.AuthorizationException("Operation not permitted for your role.")

        return current_user

    return dependency


ROLE_PERMISSIONS = {
    "SUPER_ADMIN": {
        "users": ["create", "read", "update", "delete"],
        "products": ["create", "read", "update", "delete"],
        "categories": ["create", "read", "update", "delete"],
        "product_variants": ["create", "read", "update", "delete"],
        "orders": ["create", "read", "update", "delete"],
        "payments": ["create", "read", "update", "delete"],
        "inventory": ["create", "read", "update", "delete"],
        "coupons": ["create", "read", "update", "delete"],
        "reviews": ["create", "read", "update", "delete"],
        "wishlists": ["create", "read", "update", "delete"],
        "addresses": ["create", "read", "update", "delete"],
        "cart": ["create", "read", "update", "delete"],
    },

    "MANAGER": {
        "users": ["read", "update"],
        "products": ["create", "read", "update", "delete"],
        "categories": ["create", "read", "update", "delete"],
        "product_variants": ["create", "read", "update", "delete"],
        "orders": ["read", "update"],
        "payments": ["read"],
        "inventory": ["read", "update"],
        "coupons": ["create", "read", "update"],
        "reviews": ["read", "update"],
        "wishlists": ["read"],
        "addresses": ["read"],
        "cart": ["read"],
    },

    "CATALOG_MANAGER": {
        "products": ["create", "read", "update", "delete"],
        "categories": ["create", "read", "update", "delete"],
        "product_variants": ["create", "read", "update", "delete"],
        "reviews": ["read", "update"],
        "inventory": ["read"],
    },

    "SUPPORT": {
        "users": ["read"],
        "products": ["read"],
        "categories": ["read"],
        "orders": ["read", "update"],
        "payments": ["read"],
        "reviews": ["read"],
        "addresses": ["read"],
    },

    "WAREHOUSE": {
        "products": ["read"],
        "product_variants": ["read"],
        "inventory": ["read", "update"],
        "orders": ["read", "update"],
    },

    "CUSTOMER": {
        "products": ["read"],
        "categories": ["read"],
        "product_variants": ["read"],
        "cart": ["create", "read", "update", "delete"],
        "orders": ["create", "read"],
        "payments": ["create", "read"],
        "reviews": ["create", "read", "update", "delete"],
        "wishlists": ["create", "read", "update", "delete"],
        "addresses": ["create", "read", "update", "delete"],
    },

    "VENDOR": {
        "products": ["create", "read", "update"],
        "product_variants": ["create", "read", "update"],
        "inventory": ["read", "update"],
        "orders": ["read"],
    },
}

def require_permissions(resource: str, action: str):
    def has_permission(current_user: User = Depends(get_current_user)):

        permission = ROLE_PERMISSIONS[current_user.role.name]

        allowed_actions = permission.get(resource, [])

        if action not in allowed_actions:
            raise exceptions.AuthorizationException("you don't have permit!")

        return current_user

    return has_permission
