from sqlalchemy.orm import Session
from app.schemas.product import ProductRequest, ProductUpdate
from app.models.product import Product

def create_product(db: Session, product: ProductRequest):
    try:
        new_product = Product(
            name=product.name,
            slug=product.slug,
            description=product.description,
            price=product.price,
            category_id=product.category_id
        )

        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product
    except ValueError:
        db.rollback()
        return {"message": "Value error"}
    except Exception as e:
        db.rollback()
        return {"message": f"{str(e)}"}

def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def update_product(db: Session, product_id: int, payload: ProductUpdate):
    try:
        db_product = get_product(db=db, product_id=product_id)

        if not db_product:
            return {"message": "the product does not exist in the database."}

        data = payload.model_dump(exclude_unset=True)

        for field, value in data.items():
            setattr(db_product, field, value)

        db.commit()
        db.refresh(db_product)
        return db_product
    except ValueError:
        db.rollback()
        return {"message": "please enter valid value."}
    except Exception as e:
        db.rollback()
        return {"message": f"{str(e)}"}

def delete_product(db: Session, product_id: int):
    try:
        db_product = get_product(db=db, product_id=product_id)

        if not db_product:
            return {"message": "the product does not exist"}

        db.delete(db_product)
        db.commit()
    except Exception as e:
        db.rollback()
        return {"message": f"{str(e)}"}

