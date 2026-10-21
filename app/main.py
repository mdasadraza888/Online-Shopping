from fastapi import FastAPI
from app.api.v1.endpoints.auth import router
from app.api.v1.endpoints.user import user_route
from app.api.v1.endpoints.products import product_rout
from app.core import exception_handler
from app.core import exceptions


app = FastAPI(title="E-Commerce Backend", version='1.0.0')

app.add_exception_handler(exceptions.AppException, exception_handler.app_exception_handler)
app.add_exception_handler(exceptions.AuthenticationException, exception_handler.user_authentication_handler)
app.add_exception_handler(exceptions.AuthorizationException, exception_handler.user_authorization_handler)
app.add_exception_handler(exceptions.UserNotFoundException, exception_handler.user_not_found_handler)
app.add_exception_handler(exceptions.ProductNotFoundException, exception_handler.product_not_found_handler)
app.add_exception_handler(exceptions.CategoryNotFoundException, exception_handler.category_not_found_handler)
app.add_exception_handler(exceptions.CartNotFoundException, exception_handler.cart_not_found_handler)
app.add_exception_handler(exceptions.OrderNotFoundException, exception_handler.order_not_found_handler)
app.add_exception_handler(exceptions.PaymentException, exception_handler.payment_handler)
app.add_exception_handler(exceptions.InsufficientStockException, exception_handler.insufficient_stock_handler)

app.include_router(router=router, prefix="/Auth", tags=['auth'])
app.include_router(router=user_route, prefix="/profile", tags=["Profile"])
app.include_router(router=product_rout, prefix="/Products", tags=["Products"])

@app.get("/")
def root():
    return {"message": "E-commerce Api is running"}





# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)