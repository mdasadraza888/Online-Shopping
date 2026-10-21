from app.crud import crud_products
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import product
from app.core import database
from app.core import exceptions
from app.api import deps
from app.models.user import User

product_rout = APIRouter()


@product_rout.get("/app/api/v1/endpoints/products/slug/{slug}", response_model=product.ProductResponse)
def get_product(slug: str, db: Session = Depends(database.get_db)):
    try:
        dp_product = crud_products.get_product(db=db, slug=slug)

        if not dp_product:
            raise exceptions.ProductNotFoundException("Product not found!")

        return dp_product
    except ValueError:
        db.rollback()
        raise exceptions.AppException("Provided item not found.")

@product_rout.post("/app/api/v1/endpoints/products/create-product", response_model=product.ProductResponse, dependencies=[Depends(deps.require_permissions("products", "create"))],)
def create_product(product: product.ProductRequest, db: Session = Depends(database.get_db), current_user: User = Depends(deps.get_current_user)):
    try:
        if deps.role_checker(role=current_user.role):
            raise exceptions.AuthorizationException("You have not right to perform this task")

        if not current_user:
            raise exceptions.AuthenticationException("First log in.")

        new_product = crud_products.create_product(db=db, product=product)

        if not new_product:
            raise exceptions.ProductNotFoundException("Something went wrong.")

        return new_product
    except:
        db.rollback()
        raise 

@product_rout.delete("/app/api/v1/endpoints/products/delete-product/{slug}", dependencies=[Depends(deps.require_permissions("products", "delete"))],)
def delete_product(slug: str, db: Session = Depends(database.get_db), current_user: User = Depends(deps.get_current_user)):
    try:
        if deps.role_checker(role=current_user.role):
            raise exceptions.AuthorizationException("You have not right to perform this task")

        if not current_user:
            raise exceptions.AuthenticationException("First log in.")

        msg = crud_products.delete_product(db=db, product_slug=slug)

        return {"Status": "Success", "msg": msg}
    except:
        db.rollback()
        raise

@product_rout.patch("/app/api/v1/endpoints/products/update-product/{slug}", dependencies=[Depends(deps.require_permissions("products", "update"))])
def update_product(slug: str, product: product.ProductUpdate, db: Session = Depends(database.get_db), current_user: User = Depends(deps.get_current_user)):
    try:
        if deps.role_checker(role=current_user.role):
            raise exceptions.AuthorizationException("You have not right to perform this task")

        if not current_user:
            raise exceptions.AuthenticationException("First log in.")
        
        updated_prod = crud_products.update_product(db=db, product_slug=slug, payload=product)

        if not update_product:
            raise exceptions.ProductNotFoundException("Product not found")

        return update_product
    except:
        db.rollback()
        raise 