from sqlalchemy.orm import Session
from app.schemas.user import UserRequest, UserUpdate, UserResponse
from app.models.user import User
from app.core.security import get_hash_password

def get_user(db: Session, email: str) -> UserResponse:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserRequest) -> UserResponse:
    try:
        db_user = get_user(user.email)
        if db_user:
            return {"message": "You already registered."}

        password_hash = get_hash_password(user.password)
        new_user = User(
            name=user.name,
            email=user.email,
            password=password_hash,
            phone=user.phone,
            role=user.role
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except ValueError:
        db.rollback()
        return {"status": "unsuccessfull", "message": "Please enter valid information"}
    except Exception as server_error:
        return {"status": "unsuccessfull", "message": f"{str(server_error)}"}
    finally:
        db.close()

def update_user(db: Session, email: str, payload: UserUpdate) -> UserResponse:
    try:
        db_user = get_user(email=email)
        if not db_user:
            return {"message": "The user does not exist in data."}

        data = payload.model_dump(exclude_unset=True)

        if "password" in data:
            data["password"] = get_hash_password(data.pop("password"))

        for key, value in data.items():
            setattr(db_user, key, value)

        db.commit()
        db.refresh(db_user)

        return db_user
    except ValueError:
        db.rollback()
        return {"status": "unsuccessfull", "message": "Please enter valid information"}
    except Exception as server_error:
        return {"status": "unsuccessfull", "message": f"{str(server_error)}"}

def delete_user(db: Session, email: str) -> dict:
    try:
        db_user = get_user(email=email)
        if not db_user:
            return {"message": "You account does not exist."}

        db.delete(db_user)
        db.commit()
        return {"message": "your account has been deleted."}
    except ValueError:
            db.rollback()
            return {"status": "unsuccessfull", "message": "Please enter valid information"}
    except Exception as server_error:
        return {"status": "unsuccessfull", "message": f"{str(server_error)}"}
    finally:
        db.close()

