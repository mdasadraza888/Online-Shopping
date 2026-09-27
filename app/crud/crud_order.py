from sqlalchemy.orm import Session
from app.models.order import Order, OrderStatus
from app.schemas.order import OrderRequest, OrderUpdate

def create_order(db: Session, order: OrderRequest):
    try:
        new_order = Order(
            shipping_address_id = order.shipping_address_id,
            coupon_id = order.coupon_id
        )

        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        return new_order
    except Exception as e:
        db.rollback()
        return {"message": f"{str(e)}"}

def get_order(db: Session, id: int):
    return db.query(Order).filter(Order.id == id).first()

def get_user_orders(db: Session, user_id: int):
    return db.query(Order).filter(Order.user_id == user_id).all()

def update_order_status(db: Session, order_id: int, status: OrderStatus):
    try:
        order = get_order(db=db, id=order_id)

        if not order:
            return None

        order.status = status

        db.commit()
        db.refresh(order)
        return order
    except Exception:
        db.rollback()
        raise

def cancel_order(db: Session, order_id: int):
    try:
        db_order = get_order(db=db, id=order_id)

        if not db_order:
            return None

        db_order.status = OrderStatus.CANCELLED
        db.commit()
        db.refresh(db_order)

        return db_order
    except Exception:
        db.rollback()
        raise
        