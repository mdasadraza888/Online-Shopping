from sqlalchemy.orm import Session
from app.schemas.product import ProductVariantRequest, ProductVariantUpdate
from app.models.productvariant import ProductVariant

def create_product_variant(db: Session, product_variant: ProductVariantRequest):
    try:
        new_product_variant = ProductVariant(
            product_id=product_variant.product_id,
            size=product_variant.size,
            color=product_variant.color,
            sku=product_variant.sku,
            stock=product_variant.stock
        )

        db.add(new_product_variant)
        db.commit()
        db.refresh(new_product_variant)
        return new_product_variant
    except Exception as e:
        db.rollback()
        return {"message": f"{str(e)}"}

def get_product_variant(db: Session, id: int):
    return db.query(ProductVariant).filter(ProductVariant.id == id).first()

def delete_product_variant(db: Session, id: int):
    try:
        db_product_variant = get_product_variant(db=db, id=id)

        if not db_product_variant:
            return {"message": "the product variant does not exist."}

        db.delete(db_product_variant)
        db.commit()
        return db_product_variant
    except Exception as e:
        db.rollback()
        return {"message": f"{str(e)}"}

def update_product_variant(db: Session, id: int, payload: ProductVariantUpdate):
    try:
        db_product_variant = get_product_variant(db=db, id=id)

        if not db_product_variant:
            return {"message": "the product variant does not exist"}

        data = payload.model_dump(exclude_unset=True)

        for field, value in data.items():
            setattr(db_product_variant, field, value)

        db.commit()
        db.refresh(db_product_variant)
        return db_product_variant
    except Exception as e:
        db.rollback()
        return {"message": f"{str(e)}"}